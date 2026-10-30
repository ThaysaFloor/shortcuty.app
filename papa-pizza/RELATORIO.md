# PAPA PIZZA V5.4 — entrega para reteste

## Resultado verificável

Build oficial do Shortcuty Studio, compilador 0.1.4: **1028 ações, 0 erros e 38 avisos**. Redução de 79.5% em relação às 5023 ações da V4. Os arquivos fonte/projeto e o cadastro estão vinculados às evidências por hashes no manifesto. O schema oficial também é verificado localmente.

O Check oficial deve corresponder aos mesmos arquivos; sua evidência está em `validacao/check-oficial.json`. O roteiro de verificação está em `scripts/validar.py`. Não houve assinatura ou execução da V5.4 no iPhone neste trabalho.

## Observação que motivou esta revisão

No vídeo da V5.3, não aparece novamente o alerta Massa/Massa. Após a escolha do cadastro o atalho permanece em execução e não mostra o menu durante a gravação. O usuário confirmou que continua executando sem perguntas mesmo após aguardar. A etapa exata em que a execução permanece ainda não está isolada; não se concluiu que o cadastro está incorreto.

A validação anterior de duplicatas percorria os IDs já vistos para cada produto: até 1770 comparações para 60 produtos, além das ações de leitura/conversão. A V5.4 usa consulta e inserção por chave em dicionário, mantendo a detecção de IDs repetidos sem a repetição interna. Não se faz a leitura de registros antigos em uma conferência nova, que começa vazia. São otimizações de trabalho executado, não uma medição de desempenho no aparelho.

Três avisos temporários foram adicionados somente na criação inicial: cadastro validado, JSON preparado e principal salvo/relido. Eles distinguem uma demora na validação, preparação do JSON, gravação ou entrada no menu. O último aviso exibido deve ser informado caso a execução não avance. Não são confirmações de permissão nem aparecem após cada item.

## Pastas prontas, conforme solicitado

Prepare `iCloud Drive/Atalhos/PAPA PIZZA/V5/Conferencias`, `Backups` e `Resumos`. O atalho seleciona a pasta V5 e abre as subpastas existentes, com seletor adicional desativado e erro explícito se faltarem. Nenhuma ação nativa de criação de pastas permanece no Build. Veja `PREPARAR_PASTAS.md`.

O único arquivo de consulta para começar é Papa_Pizza.json. O original permanece em Atalhos ou no local escolhido pelo usuário e não é alterado. Não é necessário criar JSON vazio, planilha, índice ou arquivo de configuração. Principal, backup e HTML são gerados pelo atalho.

## Funcionalidades preservadas

Lista alfabética dos mesmos 60 produtos e IDs; três quantidades por item, incluindo estoque zero; comprar/processar simultâneos; próximo, deixar para depois, revisar, pausar e retomar; confirmação de encerramento parcial; finalizados somente para consulta; cinco recentes e anteriores; tabela completa e listas Não conferidos/Comprar/Processar; cadastro completo em cada sessão; JSON principal e backup anterior; recuperação em nova conferência; independência de Lembretes.

O armazenamento permanece no formato JSON V5. Os registros são strings JSON por ID para respeitar o contrato Text de data.set_value. Ausência de chave significa não conferido. Revisão substitui a chave e não cria duplicata.

O backup é escrito e relido antes de atualizar o principal. O hash detecta alterações do principal desde a leitura antes de iniciar a substituição. Não há transação atômica ou bloqueio distribuído: use uma execução por conferência. Falhas nativas de iCloud podem interromper o atalho e requerer recuperação manual; o backup pode perder o checkpoint mais recente.

## Evidências de integridade

Cadastro original preservado byte a byte, SHA-256 `b93b0daad59e491e88f6692d7ee22a3c5fa2c8851c8a55052cbdff4bba8b858b`: 60 IDs únicos e nove grupos. Os grupos continuam no arquivo e fora da interface. A referência exportada pelo compilador coincide com todos os pares ID/nome do original.

As nove comparações restantes entre variáveis de texto mantêm WFTextTokenString, com referências dinâmicas. A comparação de duplicatas por texto foi substituída pela presença da chave no dicionário. Não houve supressão de avisos, remoção da validação do cadastro ou uso de native_action para contornar o checker.

## Limites

V5.4 é uma revisão de diagnóstico ainda pendente de teste no iPhone. Abrir subpastas como referências de folder, materializar arquivos, JSON vazio, nomes/extensões, Unicode, backup, retomada, HTML e desempenho ainda precisam ser validados. O Build não homologa a execução. A compatibilidade mínima de iOS permanece parcialmente desconhecida no catálogo oficial.

O loop do fluxo é limitado a 1000 interações; pausar e finalizar usam flow.stop imediato. Ao atingir o limite, a execução avisa e pode ser retomada. Não se usa recursão. Arquivos V3/V4 e pastas antigas permanecem sem alteração e não aparecem no histórico V5.

## Avisos oficiais

- **4**: files.open.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **6**: data.decode_json.input expects Dictionary, got Text. Shortcuts supports this content conversion; success still depends on the input at runtime.
- **2**: files.contents.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: chooseFromList.WFInput expects Any | Dictionary | Image, got List<Text | Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Native<WFFolderContentItem> to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **5**: count.Input expects Any | Text, got List<Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **9**: condition.WFConditionalActionString expects Value, got Text. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **3**: setVariable: cannot verify conversion from Value to Dictionary; the cast will be attempted at runtime. Verify the producer type and test this input.
- **1**: count.Input expects Any | Text, got Value. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFConditionalActionString expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFNumberValue expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Value to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **3**: files.save.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.

A mudança para referências de pastas abertas por files.open acrescenta avisos de File | Native<WFFolderContentItem>. Eles foram mantidos e precisam de confirmação no aparelho; não são prova de segurança ou de falha.
