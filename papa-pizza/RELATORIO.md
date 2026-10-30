# Revisão aprovada — PAPA PIZZA V5.2

## Resultado real

O projeto foi submetido ao Check e ao Build oficiais do Shortcuty Studio, compilador 0.1.4. Ambos concluíram sem erros, com 31 avisos. O Build gerou **1,191 ações nativas**, contra 5.023 da V4: redução de **79.7%**. Ainda é um fluxo com mais de mil ações; rapidez e memória no iPhone permanecem desconhecidas.

Evidências completas em `validacao/build-oficial.json`, `check-oficial.json`, `diagnosticos.json` e `manifesto.json`. O manifesto vincula as evidências aos hashes do código, projeto e cadastro. O schema oficial do projeto também foi validado.

A V5.2 não foi executada em iPhone, assinada ou instalada neste trabalho. O vídeo enviado pelo usuário mostrou a V5 falhando na preparação de pastas, antes de abrir o cadastro. A compatibilidade de versão mínima do iOS no resultado oficial é parcial; não há versão mínima comprovada para o conjunto.

## Proposta implementada

1. Lista alfabética única dos mesmos 60 produtos, com IDs originais. Grupos retirados da interface e preservados no cadastro e na cópia histórica.
2. Estoque atual, quantidade para comprar e quantidade para processar, sem perguntas redundantes de OK/Pendência ou Sim/Não. Compra e processamento podem coexistir. Zero é válido; ausência de registro indica não conferido.
3. Próximo item, deixar para depois, revisar qualquer item, pausar e finalizar. Retomada no primeiro não conferido; uma revisão substitui a chave do ID.
4. Confirmação de encerramento mostrando quantos itens faltam. Encerramento parcial permitido e marcado FINALIZADA. Conferências encerradas ficam somente para consulta.
5. Tabela completa com 60 linhas e três listas: Não conferidos, Comprar e Processar. Itens OK continuam visíveis. Quantidades entre produtos não são somadas.
6. Um JSON principal e um backup anterior por conferência; gravação após cada item completo. O backup é gravado e relido antes do principal. O hash detecta mudanças do principal desde sua leitura antes de iniciar a substituição.
7. Recuperação por backup em nova conferência, preservando o principal problemático. Históricos anteriores e cadastro original não são apagados.
8. Cinco conferências mais recentes e acesso às anteriores.
9. Cópia do cadastro completo em cada sessão, para manter o significado dos históricos.
10. Sem Lembretes, aplicações de terceiros, filtros interativos ou edição de sessões encerradas.

## Redução de complexidade

Foi eliminada a reconstrução reiterada de listas/grupos e o salvamento duplicado em vários pontos. Há um único checkpoint no fluxo, com três pontos nativos de escrita: backup, principal e HTML. A estrutura por ID permite atualizar o item com `data.set_value`, usando seu contrato documentado de valor Text. Por isso cada linha é uma string JSON com três quantidades dentro do dicionário de registros; não foi forçada uma conexão Dictionary -> Text incompatível.

Na V5.2 não há funções auxiliares definidas pelo projeto: leitura, entrada, gravação, data e escape usam ações diretas. O compilador ainda emite Set Variable para atribuições comuns; a contagem permanece acima de mil ações. A contagem de ações mede o grafo nativo, não o tempo de execução. O repeat de até 1000 interações não é 1000 cópias desse grafo; pausar/finalizar executam flow.stop imediatamente. No limite, o progresso já salvo pode ser retomado em outra execução.

## Dados preservados e pastas

`Papa_Pizza.json` foi copiado byte a byte, SHA-256 `b93b0daad59e491e88f6692d7ee22a3c5fa2c8851c8a55052cbdff4bba8b858b`: 60 IDs únicos e nove grupos. A ordem está em `ordem.json` e foi gerada ignorando acentos para comparação alfabética. IDs e nomes são conferidos ao abrir a sessão; uma alteração de cadastro exige nova geração do projeto.

A V5 usa `PAPA PIZZA/V5/Conferencias`, `Backups` e `Resumos` dentro de uma pasta-base existente selecionada explicitamente no iCloud Drive. Os níveis são criados sequencialmente, sem dependência da raiz implícita Atalhos. Use a mesma base para reencontrar o histórico. Arquivos V3/V4 permanecem em suas pastas antigas, sem migração automática; não aparecem no histórico V5.

## Limites e testes pendentes

- Não há transação atômica ou bloqueio distribuído no iCloud. Use um gravador por conferência. Uma alteração concorrente entre a verificação do hash e a escrita ainda pode gerar conflito.
- Um backup guarda o checkpoint anterior, não todo o histórico de alterações. Se a última gravação principal falhar, o item mais recente pode precisar ser conferido novamente.
- Uma falha nativa de leitura/gravação pode interromper o atalho; a recuperação é escolhida manualmente na próxima execução.
- Entrada inválida ou cancelamento antes de completar as três perguntas não grava aquele item; os anteriores permanecem.
- Materialização de Text em File por files.convert, nomes/extensões, JSON com objetos vazios, acentos, leitura/escrita do iCloud e abertura do HTML exigem teste real.
- Não houve supressão de avisos, emprego de native_action para contornar o checker ou declaração de sucesso no iPhone. O roteiro completo está em `TESTES_IPHONE.md`.

## Regressão de pastas corrigida na V5.1

O vídeo mostrou o erro nativo “A localização não existe” no início da V5. Não houve evidência de leitura do cadastro ou gravação de conferência naquele teste. A causa exata entre a raiz implícita e os caminhos intermediários não pode ser isolada apenas pelo vídeo. A correção remove ambas as dependências: o usuário escolhe uma pasta-base existente e cada criação recebe explicitamente o resultado da pasta pai. Foram acrescentadas duas criações e um seletor de base; na V5.1, o Build passou de 1.179 para 1.191 ações. Não foi validada a execução corrigida no iPhone.

## Reteste de leitura na V5.2

O segundo vídeo mostra a V5.1 chegando à escolha do JSON e, depois, à mensagem Cadastro divergente. A tabela de referência do grafo nativo coincide com os 60 pares ID/nome do JSON recebido. Isso não determina quais valores foram efetivamente lidos no aparelho e não prova uma divergência real do cadastro.

Foram removidas funções auxiliares de leitura/retorno e substituídas todas as condições and/or por If simples. A validação continua presente, separada em ID ausente na referência e nome diferente, com diagnóstico dos valores lidos e esperados antes de qualquer gravação. Não houve mudança do cadastro, do formato de armazenamento V5, das pastas, do backup ou das funcionalidades aprovadas. Trata-se de uma revisão para reteste; a causa nativa exata ainda não está comprovada.

Ações nativas: V4 5.023 → V5 1.179 → V5.1 1.191 → V5.2 1.018. Os helpers removidos já não geram argumentos/retornos privados no grafo. A contagem não comprova desempenho no iPhone.

## Avisos oficiais pendentes

- **1**: files.create_folder.folder expects File, got File | Native<WFFolderContentItem>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **6**: data.decode_json.input expects Dictionary, got Text. Shortcuts supports this content conversion; success still depends on the input at runtime.
- **1**: chooseFromList.WFInput expects Any | Dictionary | Image, got List<Text | Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Native<WFFolderContentItem> to File; the cast will be attempted at runtime. Verify the producer type and test this input.
- **5**: count.Input expects Any | Text, got List<Value>. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **10**: condition.WFConditionalActionString expects Value, got Text. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **3**: setVariable: cannot verify conversion from Value to Dictionary; the cast will be attempted at runtime. Verify the producer type and test this input.
- **1**: count.Input expects Any | Text, got Value. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFConditionalActionString expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: condition.WFNumberValue expects Value, got Number. Compatibility is unknown; add a declared type or explicit supported conversion and test the input.
- **1**: setVariable: cannot verify conversion from File | Value to File; the cast will be attempted at runtime. Verify the producer type and test this input.

Os avisos não foram suprimidos. Conversões declaradas e contratos desconhecidos permanecem sujeitos a teste no aparelho.
