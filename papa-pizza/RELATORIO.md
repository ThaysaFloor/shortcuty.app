# PAPA PIZZA V5.5 — entrega para reteste

## Resultado verificável

Build oficial do Shortcuty Studio, compilador 0.1.4: **1108 ações, 0 erros e 43 avisos**. Redução de 77.9% em relação às 5023 ações da V4. O Check oficial deve corresponder aos mesmos arquivos; as evidências e hashes estão em validacao/. O schema oficial e o grafo nativo são verificados por scripts/validar.py.

A V5.5 não foi executada no iPhone, assinada ou instalada neste trabalho. O reteste é obrigatório. Não houve supressão de avisos ou declaração de execução bem-sucedida desta revisão.

## Evidência de execução recebida

O trecho completo da V5.4 mostra o aviso 3/3, o menu alfabético e as três perguntas do primeiro produto. Portanto o JSON inicial foi gravado e relido, e o fluxo chegou à entrada de quantidades. Depois apareceu Principal ausente: a rotina não reencontrou o arquivo por nome e concluiu indevidamente que havia sido removido. Não há evidência de exclusão pelo usuário no vídeo.

O usuário informou nomes como Conferencia_-numero.txt: extensão TXT e ausência da data no nome. A exportação anterior da ação de data não continha WFDateActionMode explícito. O Save recebia arquivo materializado como texto simples sem uma ação Set Name anterior. Isso motivou correções concretas de data, nome e identidade do arquivo, mas não comprova ainda sua execução corrigida no dispositivo.

## Correções V5.5

- A data é obtida com dates.value(date_action_mode: "Current Date"). O grafo contém explicitamente WFDateActionMode=Current Date nas duas ações de data, em vez de depender de um padrão implícito.
- O resultado formatado deve corresponder a yyyy-MM-dd_HH-mm-ss-SSS. Se estiver vazio ou incompleto, o atalho para antes de criar um nome de conferência ou resumo inválido.
- O arquivo temporário materializado por files.convert recebe Set Name com extensão incluída antes do Save. Isso é feito para principal, backup e HTML; nenhum arquivo histórico é renomeado por essa ação.
- Depois de cada Save, a extensão é verificada: json para principal/backup e html para resumo. Uma divergência para a execução e mostra a extensão observada. A releitura do conteúdo continua presente.
- A referência do arquivo retornada por Save é mantida em arquivoPrincipal após a verificação. Retomadas normais usam a referência do arquivo aberto. Atualizações não procuram novamente o principal pelo nome; a listagem por nome fica restrita à checagem de colisão na criação.
- Antes de atualizar, o hash da referência é comparado ao último hash, e o conteúdo anterior é gravado/relido no backup. O controle é de melhor esforço: cache de conteúdo ou sincronização do iCloud podem limitar a observação de alterações externas. Não há bloqueio ou transação distribuída; use uma execução por conferência de cada vez.
- O histórico usa a extensão real e reconstrói o nome completo quando Get Name retorna só o nome sem extensão. Arquivos TXT antigos ficam preservados e fora do histórico JSON. Não há conversão ou exclusão automática deles.

## Funcionalidades preservadas

60 produtos e IDs originais em ordem alfabética; estoque atual, comprar e processar; zero válido; pendências simultâneas; deixar para depois, revisar, pausar e retomar; confirmação de encerramento parcial; finalizados somente para consulta; cinco recentes e anteriores; tabela completa e listas Não conferidos/Comprar/Processar; cadastro completo em cada sessão; um principal e um backup anterior; recuperação em nova conferência; sem dependência de Lembretes.

Os registros permanecem strings JSON por ID, respeitando o contrato Text de data.set_value. Ausência significa não conferido. A revisão substitui a chave e não duplica o produto.

## Pastas e dados

Use as pastas já prontas iCloud Drive/Atalhos/PAPA PIZZA/V5/Conferencias, Backups e Resumos. Selecione V5 no primeiro seletor. Papa_Pizza.json original pode permanecer em Atalhos. Não há criação automática de pastas nem outro arquivo inicial obrigatório.

Cadastro preservado byte a byte, SHA-256 `b93b0daad59e491e88f6692d7ee22a3c5fa2c8851c8a55052cbdff4bba8b858b`: 60 IDs únicos e nove grupos, com referência exportada conferida contra o original. O JSON original não é gravado pelo atalho.

Mantenha os .txt produzidos nos testes; a V5.5 não os renomeia nem os migra automaticamente. Como nomes/IDs desses arquivos podem estar incompletos, comece o reteste com Nova conferência. O erro da V5.4 ocorreu antes de gravar o primeiro item recebido; não há confirmação de que aquelas respostas tenham sido persistidas.

## Reteste necessário

1. Nova conferência: selecionar V5 e o mesmo JSON original, acompanhar 1/3, 2/3 e 3/3.
2. Verificar que o novo arquivo tem data/hora e extensão .json.
3. Conferir um produto com as três quantidades; verificar que o principal e o backup continuam na pasta certa.
4. Pausar, retomar e revisar o mesmo produto sem duplicação; conferir JSON e contador.
5. Finalizar e gerar HTML com extensão .html e abertura visual correta.
6. Se aparecer Data indisponível, Nome do arquivo ou Referência indisponível, registrar a mensagem e preservar todos os arquivos.

O roteiro completo continua em TESTES_IPHONE.md. A compatibilidade mínima de iOS é parcialmente desconhecida no catálogo; o Build não certifica permissões, formato físico, cache, desempenho ou execução de ações nativas.

## Diagnóstico temporário e limites

Os três avisos de inicialização permanecem temporariamente para localizar a etapa no iPhone. Há limite de 1000 interações por execução; pausar/finalizar param imediatamente com flow.stop. O progresso pode ser retomado se o limite for alcançado. Não há recursão ou exclusão de históricos. A validação de IDs usa dicionário e não a varredura quadrática anterior; conferências novas não leem registros antigos vazios.

## Avisos oficiais

- **4**: files.open.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **6**: data.decode_json.input expects Dictionary, got Text. Shortcuts supports this content conversion; success still depends on the input at runtime.
- **2**: files.contents.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: chooseFromList.WFInput expects Any | Dictionary | Image, got List<Text | Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Native<WFFolderContentItem> to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **7**: count.Input expects Any | Text, got List<Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **9**: condition.WFConditionalActionString expects Value, got Text. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **3**: setVariable: cannot verify conversion from Value to Dictionary; the cast will be attempted at runtime. Verify the producer type and test this input.
- **1**: count.Input expects Any | Text, got Value. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFConditionalActionString expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFNumberValue expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Value to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **3**: setVariable: cannot verify conversion from Value to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **3**: files.save.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.

Os casts de saída Value de Set Name para File refletem uma lacuna de metadados: o produtor é um arquivo materializado que recebeu nome, mas a execução ainda precisa confirmar a conversão. Não foi usado cast para inventar dados nem para substituir a ação de nomeação.
