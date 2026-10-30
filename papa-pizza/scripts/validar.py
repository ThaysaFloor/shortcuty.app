"""Verify delivery evidence and native wiring; does not execute Apple actions."""
from pathlib import Path
import collections
import hashlib
import json
import unicodedata

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def validate():
    project = load("PAPA_PIZZA_V5.shortcutystudio.json")
    schema = load("validacao/schema.project.json")
    jsonschema.Draft202012Validator(schema).validate(project)
    source = (ROOT / "PAPA_PIZZA_V5.shortcuty").read_text()
    assert project["files"] == [{"name": "Main.shortcuty", "contents": source}]
    assert (ROOT / "PAPA_PIZZA_V5.shortcutystudio").read_bytes() == (
        ROOT / "PAPA_PIZZA_V5.shortcutystudio.json"
    ).read_bytes()
    print("PASS: official project schema and identical source/project copies")

    manifest = load("validacao/manifesto.json")
    assert digest("PAPA_PIZZA_V5.shortcuty") == manifest["source_sha256"]
    assert digest("PAPA_PIZZA_V5.shortcutystudio.json") == manifest["project_sha256"]
    assert digest("Papa_Pizza.json") == manifest["cadastro_sha256"]
    assert manifest["cadastro_sha256"] == "b93b0daad59e491e88f6692d7ee22a3c5fa2c8851c8a55052cbdff4bba8b858b"
    print("PASS: compiled source/project fingerprints and unmodified original catalog")

    products = load("Papa_Pizza.json")["itens"]
    assert len(products) == len({p["id"] for p in products}) == 60
    assert len({p["categoria"] for p in products}) == 9
    alphabetical = sorted(products, key=lambda p: unicodedata.normalize("NFD", p["nome"]).encode("ascii", "ignore").decode().casefold())
    assert load("ordem.json") == [{"id": p["id"], "nome": p["nome"]} for p in alphabetical]
    print("PASS: 60 unique IDs, nine preserved groups and alphabetical ordering")

    result = load("validacao/build-oficial.json")
    assert result["ok"] is True
    assert not any(d["severity"] == "error" for d in result["diagnostics"])
    assert result["diagnostics"] == load("validacao/diagnosticos.json")
    actions = result["actions"]
    assert len(actions) == manifest["actions"] < manifest["baseline_v4_actions"]
    assert len(result["diagnostics"]) == manifest["warnings"]
    print(f"PASS: official Build, {len(actions)} actions, {manifest['warnings']} warnings, no errors")

    by_uuid = {a["parameters"]["UUID"]: a for a in actions if "UUID" in a["parameters"]}
    assert len(by_uuid) == sum("UUID" in a["parameters"] for a in actions)
    refs = set()

    def references(value):
        if isinstance(value, dict):
            if "OutputUUID" in value:
                refs.add(value["OutputUUID"])
            for child in value.values():
                references(child)
        elif isinstance(value, list):
            for child in value:
                references(child)

    for action in actions:
        references(action["parameters"])
    assert refs <= by_uuid.keys(), refs - by_uuid.keys()
    print("PASS: unique action identities and resolved native producer references")

    reference_assignment = next(
        a for a in actions
        if a["call"] == "variables.set"
        and a["parameters"].get("WFVariableName") == "referencia"
    )
    reference_uuid = reference_assignment["parameters"]["WFInput"]["Value"]["OutputUUID"]
    reference_items = by_uuid[reference_uuid]["parameters"]["WFItems"]["Value"]["WFDictionaryFieldValueItems"]
    exported_reference = {
        row["WFKey"]["Value"]["string"]: row["WFValue"]["Value"]["string"]
        for row in reference_items
    }
    assert exported_reference == {str(p["id"]): p["nome"] for p in products}
    direct_product_keys = {
        a["parameters"].get("WFDictionaryKey")
        for a in actions
        if a["call"] == "data.lookup"
        and isinstance(a["parameters"].get("WFDictionaryKey"), str)
        and a["parameters"].get("WFInput", {}).get("Value", {}).get("VariableName") == "produto"
    }
    assert {"id", "nome"} <= direct_product_keys
    assert not any("WFConditions" in a["parameters"] for a in actions if a["call"] == "flow.condition")
    print("PASS: original ID/name table exported intact, direct field reads and simple If conditions")

    text_comparisons = [
        a["parameters"]["WFConditionalActionString"]
        for a in actions
        if a["call"] == "flow.condition"
        and isinstance(a["parameters"].get("WFConditionalActionString"), dict)
    ]
    assert len(text_comparisons) == 9
    comparison_variables = set()
    for operand in text_comparisons:
        assert operand["WFSerializationType"] == "WFTextTokenString"
        value = operand["Value"]
        assert isinstance(value["string"], str)
        attachments = value["attachmentsByRange"]
        assert attachments
        comparison_variables.update(token["VariableName"] for token in attachments.values())
    assert comparison_variables == {
        "nomeEsperado", "esperado", "nomeAtual", "identificador",
        "nomeSessao", "ultimoHash", "ultimoJson", "novoJson", "html"
    }
    print("PASS: all 9 dynamic text comparison operands use token strings, preserving their variables")

    current_dates = [a for a in actions if a["identifier"] == "is.workflow.actions.date"]
    assert len(current_dates) == 2
    assert all(a["parameters"]["WFDateActionMode"] == "Current Date" for a in current_dates)
    renamed = [a for a in actions if a["call"] == "files.rename"]
    assert len(renamed) == 3
    assert all(a["parameters"]["WFDontIncludeFileExtension"] is False for a in renamed)
    assert {
        a["parameters"]["WFInput"]["Value"]["VariableName"] for a in renamed
    } == {"convertido_5", "convertido_6", "convertido_11"}
    extension_guards = [
        a for a in actions if a["call"] == "flow.condition"
        and a["parameters"].get("WFConditionalActionString") in ("json", "html")
        and a["parameters"].get("WFCondition") == 5
    ]
    assert len(extension_guards) == 3
    print("PASS: explicit Current Date mode, temporary files named before saving and extension guards")

    groups = collections.defaultdict(collections.Counter)
    for action in actions:
        params = action["parameters"]
        if "GroupingIdentifier" in params:
            groups[params["GroupingIdentifier"]][params.get("WFControlFlowMode", 0)] += 1
    assert all(modes[0] == 1 and modes[2] == 1 for modes in groups.values())
    print("PASS: balanced native control groups")

    def origin(reference):
        value = reference.get("Value", reference)
        if value.get("Type") == "Variable":
            return value["VariableName"]
        action = by_uuid[value["OutputUUID"]]
        assert action["call"] == "variables.set"
        return origin(action["parameters"]["WFInput"])

    assert not any(a["call"] == "files.create_folder" for a in actions)
    folder_reads = [
        a for a in actions
        if a["call"] == "files.open"
        and a["parameters"].get("WFGetFilePath") in ("Conferencias", "Backups", "Resumos")
    ]
    assert [a["parameters"]["WFGetFilePath"] for a in folder_reads] == ["Conferencias", "Backups", "Resumos"]
    assert all(origin(a["parameters"]["WFFile"]) == "base" for a in folder_reads)
    assert all(a["parameters"]["WFShowFilePicker"] is False for a in folder_reads)
    assert all(a["parameters"]["WFFileErrorIfNotFound"] is True for a in folder_reads)
    pickers = [a for a in actions if a["call"] == "files.choose"]
    assert pickers[0]["parameters"]["WFPickingMode"] == "Folders"
    assert pickers[0]["index"] < folder_reads[0]["index"]
    print("PASS: user-selected base, three existing subfolders, no automatic folder creation")

    repeats = [a for a in actions if a["call"] == "flow.repeat_each"]
    assert not any(
        a["parameters"].get("WFInput", {}).get("Value", {}).get("VariableName") == "idsVistos"
        for a in repeats
    )
    duplicate_updates = [
        a for a in actions if a["call"] == "data.set_value"
        and a["parameters"].get("WFDictionary", {}).get("Value", {}).get("VariableName") == "idsVistos"
    ]
    assert len(duplicate_updates) == 1
    row_validation = next(
        a for a in repeats
        if a["parameters"].get("WFControlFlowMode", 0) == 0
        and a["parameters"].get("WFInput", {}).get("Value", {}).get("VariableName") == "ordem"
    )
    saved_guard = next(
        a for a in actions if a["call"] == "flow.condition"
        and a["parameters"].get("WFCondition") == 5
        and a["parameters"].get("WFConditionalActionString") == "NOVA"
    )
    guard_end = next(
        a for a in actions
        if a["parameters"].get("GroupingIdentifier") == saved_guard["parameters"]["GroupingIdentifier"]
        and a["parameters"].get("WFControlFlowMode") == 2
    )
    assert saved_guard["index"] < row_validation["index"] < guard_end["index"]
    print("PASS: duplicate IDs use dictionary updates; saved-row validation is skipped for new sessions")

    saves = [a for a in actions if a["call"] == "files.save"]
    assert len(saves) == 3
    assert [origin(a["parameters"]["WFFolder"]) for a in saves] == ["backups", "pasta", "resumos"]
    assert saves[0]["index"] < saves[1]["index"] < saves[2]["index"]
    assert all(a["parameters"]["WFAskWhereToSave"] is False for a in saves)
    assert not any(a["call"] in {"files.delete", "shortcuts.run_self", "reminders.create"} for a in actions)
    print("PASS: backup precedes principal, only three save sites, no deletion/recursion/Reminders")

    principal_assignments = [
        a for a in actions if a["call"] == "variables.set"
        and a["parameters"].get("WFVariableName") == "arquivoPrincipal"
    ]
    assert any(
        a["parameters"]["WFInput"]["Value"].get("VariableName") == "arquivoLido"
        for a in principal_assignments
    )
    assert any(
        a["parameters"]["WFInput"]["Value"].get("VariableName") == "principalGravado"
        for a in principal_assignments
    )
    principal_guard = next(
        a for a in actions if a["call"] == "flow.condition"
        and a["parameters"].get("WFCondition") == 100
        and a["parameters"].get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName") == "arquivoPrincipal"
    )
    branch_markers = [
        a for a in actions
        if a["parameters"].get("GroupingIdentifier") == principal_guard["parameters"]["GroupingIdentifier"]
    ]
    otherwise = next(a for a in branch_markers if a["parameters"].get("WFControlFlowMode") == 1)
    end = next(a for a in branch_markers if a["parameters"].get("WFControlFlowMode") == 2)
    assert principal_guard["index"] < saves[0]["index"] < otherwise["index"]
    creation_listing = next(
        a for a in actions if a["call"] == "files.contents"
        and a["parameters"].get("WFFolder", {}).get("Value", {}).get("VariableName") == "pasta"
    )
    assert otherwise["index"] < creation_listing["index"] < end["index"] < saves[1]["index"]
    print("PASS: active updates use the saved/opened file reference; directory-name lookup only on creation")
    print("PENDING: real iPhone/iCloud execution, runtime conversions, performance and signing")


if __name__ == "__main__":
    validate()
