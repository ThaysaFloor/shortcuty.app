# PAPA PIZZA V5.4

## Usar no Studio

1. Baixe `PAPA_PIZZA_V5.shortcutystudio` deste repositório e importe no [Shortcuty Studio](https://studio.shortcuty.app/). A cópia `.shortcutystudio.json` contém exatamente o mesmo projeto.
2. Se a importação não estiver disponível, crie um projeto, substitua todo o conteúdo de `Main.shortcuty` pelo arquivo `PAPA_PIZZA_V5.shortcuty` e defina o nome como **PAPA PIZZA V5.4** em Shortcut details.
3. Execute **Check** e **Build**. Revise os avisos; o resultado esperado está em `validacao/`.
4. Exporte o projeto pelo Studio. Depois de revisar o fluxo nativo, use o Download do Studio para assinar e instalar.
5. Primeiro teste com uma cópia do cadastro e dados descartáveis. Não use como registro de produção até concluir o roteiro em `TESTES_IPHONE.md`.

## Fluxo aprovado

- Os mesmos 60 produtos, em ordem alfabética, com IDs originais.
- Três quantidades por item: estoque atual, comprar e processar. As três respostas precisam ser inteiros entre 0 e 999999999; zero significa nenhuma pendência.
- Um item só fica conferido após as três respostas e o salvamento. Um estoque zero é um valor válido.
- Próximo item, deixar para depois, revisar qualquer item, pausar e finalizar.
- Ao retomar, procura o primeiro item não conferido. Dentro da execução, deixar para depois avança e volta aos pendentes quando chega ao final da lista.
- Revisar substitui o registro daquele ID; não acrescenta uma duplicata.
- Finalizar pede confirmação e mostra quantos itens faltam. Conferências encerradas são somente para consulta, mesmo quando parciais.
- Resumo com tabela completa e listas **Não conferidos**, **Comprar** e **Processar**. Um produto pode aparecer nas duas listas de pendências. Itens OK continuam na tabela.
- Cinco conferências recentes, acesso às anteriores e recuperação por backup.
- Independência do aplicativo Lembretes.

## Arquivos e recuperação

Prepare antes a estrutura de [PREPARAR_PASTAS.md](PREPARAR_PASTAS.md). O único arquivo de entrada é o `Papa_Pizza.json` original, que pode continuar em Atalhos.

Depois do menu, selecione **a pasta V5**, em `iCloud Drive/Atalhos/PAPA PIZZA/V5`, e use sempre a mesma pasta. A V5.4 apenas abre suas três subpastas existentes; não cria pastas automaticamente:

```text
iCloud Drive/Atalhos/
  Papa_Pizza.json
  PAPA PIZZA/V5/
    Conferencias/
    Backups/
    Resumos/
```

Se já existirem pastas ou arquivos, preserve-os. Não selecione Atalhos como base na V5.4; selecione V5. O JSON original nunca é gravado pelo atalho. Nenhum outro arquivo de consulta é necessário: os arquivos das conferências e os resumos são gerados durante o uso.

Existe um JSON principal por conferência e, após a primeira atualização, um backup. Antes de substituir o principal, o atalho verifica seu hash, grava o conteúdo anterior no backup e confere a releitura. Só depois grava e relê o principal. O backup guarda a versão anterior ao último checkpoint, não todas as alterações intermediárias.

Se o principal estiver corrompido, execute **Continuar conferência → Recuperar backup**. A recuperação cria outra conferência com novo ID, preservando o principal problemático e registrando sua origem. O backup pode perder as respostas do checkpoint mais recente.

Uma falha nativa do iCloud pode encerrar o atalho antes de uma mensagem personalizada. Não há transação atômica entre principal e backup, nem bloqueio distribuído entre dispositivos: use uma execução por conferência de cada vez.

Os arquivos V3/V4 permanecem nas pastas antigas e não são convertidos ou apagados. A lista de histórico da V5 mostra apenas a pasta V5. Para consultar arquivos anteriores, mantenha a versão que os gerou.

## Formato do JSON

O documento contém `versao`, `id`, `inicio`, `estado`, `origem`, `cadastro` e `registros`. `cadastro` é uma cópia do JSON original completo, incluindo os grupos, que ficam fora da interface.

`registros` é um dicionário por ID. Cada valor é uma string JSON com as três quantidades. Isso permite usar `data.set_value` com seu contrato documentado de valor Text, sem forçar um Dictionary num parâmetro Text:

```json
{
  "1": "{\"estoque\":\"20\",\"comprar\":\"40\",\"processar\":\"40\"}"
}
```

Um ID ausente significa não conferido. O formato distingue ausência de zero sem flags redundantes. As quantidades são guardadas como strings de dígitos e interpretadas numericamente para filtrar pendências.

## Manutenção e limites

A ordem alfabética foi gerada a partir do cadastro original e está documentada em `ordem.json`. A V5 confere os 60 IDs e nomes ao abrir o cadastro ou a sessão. Para mudar nomes ou produtos, gere outra versão do projeto; não altere apenas a lista embutida. Categorias e demais informações do cadastro são preservadas no JSON, embora não apareçam na navegação.

A linguagem não documenta `while` ou `break`. O fluxo usa um repeat nativo de até 1000 interações. Pausar e finalizar param imediatamente com `flow.stop()`; se o limite for atingido, avisa e permite retomar em outra execução. A repetição não duplica o código-fonte 1000 vezes no Build.

Ainda há avisos e mais de mil ações. O Build confirma compilação, não rapidez ou funcionamento no iPhone. As evidências e limites estão em `RELATORIO.md`.

## Correção V5.1 após teste no iPhone

O vídeo da V5 mostrou “A localização não existe” antes de abrir o cadastro, na preparação de pastas. Foram removidas a raiz implícita “Atalhos” e as três criações de caminhos completos com pais possivelmente ausentes. Agora há seleção explícita da base e cinco criações encadeadas: PAPA PIZZA → V5 → Conferencias/Backups/Resumos. O vídeo não distingue se a causa original foi a raiz ou o caminho intermediário. A V5.1 compilou, mas a correção precisa ser confirmada no iPhone. Os nomes dos arquivos distribuídos e o formato JSON V5 foram mantidos para preservar os links e a compatibilidade.

## Reteste V5.2 após “Cadastro divergente”

O vídeo da V5.1 avançou pela preparação de pastas e seleção do JSON, mas parou na comparação dos produtos. Isso não comprova que o arquivo do usuário esteja incorreto. A V5.2 substitui as funções auxiliares por ações nativas diretas e os predicados compostos por blocos If simples, mantendo a validação. Se houver divergência, a mensagem informa o ID, nome lido e nome esperado. A causa de execução ainda precisa ser isolada no iPhone; o Build não comprova a correção. Nenhum produto foi renomeado ou removido.

## Comparações textuais na V5.3

O vídeo da V5.2 mostrou ID 1 e Massa nos dois nomes, seguido da condição de divergência. A V5.3 mantém a validação e escreve o operando direito das dez comparações entre variáveis de texto como uma string interpolada. O grafo oficial agora usa WFTextTokenString nessas entradas WFConditionalActionString, em vez de WFTextTokenAttachment. Isso alcança nomes, IDs, hash e releitura de arquivos. O teste estático verifica esse formato, mas o comportamento no iPhone ainda precisa ser confirmado. O cadastro e o formato de armazenamento não mudaram.

## Reteste V5.4

A checagem de IDs repetidos agora usa um dicionário em vez de uma varredura de todos os IDs anteriores; não há mais até 1770 comparações na entrada dos 60 produtos. Conferências novas não percorrem registros antigos, porque começam vazias. Isso reduz o trabalho de execução, mas ainda não foi cronometrado no aparelho.

Nesta versão de diagnóstico, uma conferência nova exibe temporariamente **1/3 Cadastro validado**, **2/3 JSON preparado** e **3/3 Arquivo inicial salvo e relido**. Toque OK em cada etapa. Se continuar executando sem abrir o menu, informe o último número que apareceu. Essas mensagens não reaparecem a cada item e não substituem testes de gravação, pausa e recuperação.
