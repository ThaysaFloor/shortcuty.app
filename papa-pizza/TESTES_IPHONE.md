# Validação obrigatória no iPhone

Este roteiro ainda não foi concluído. O usuário executou a V5 e enviou vídeo do erro “A localização não existe” na preparação de pastas. O segundo vídeo mostra a V5.1 avançando pela seleção de pastas e JSON, seguida da mensagem Cadastro divergente. A revisão V5.2 ainda precisa ser executada no iPhone. Use dados descartáveis, mantenha cópias do cadastro e dos históricos e confirme a pasta do iCloud antes de começar.

1. **Instalação e abertura:** importar no Studio, executar Check/Build, revisar os avisos e assinar pelo Download. Confirmar abertura no iPhone e permissões do iCloud.
2. **Cadastro:** selecionar uma cópia de `Papa_Pizza.json`. Conferir os 60 nomes e a ordem alfabética, especialmente nomes com acentos. Comparar o arquivo original antes/depois; ele deve permanecer idêntico.
3. **Criação:** iniciar uma conferência e pausar sem conferir itens. Verificar JSON válido com `registros` vazio e cópia integral de `cadastro`. Retomar deve oferecer o primeiro produto.
4. **Zero e preenchimento:** conferir um item com estoque zero e sem pendências. Verificar a presença das três quantidades e o contador incrementado uma única vez. Na tabela, deve aparecer S; não pode parecer não conferido.
5. **Pendências simultâneas:** conferir estoque 20, compra 40 e processamento 40. Verificar ambas as listas e a tabela, com os mesmos números no JSON.
6. **Validação:** tentar vazio, negativo, decimal, letras e mais de nove dígitos. O item atual não deve ser salvo e os anteriores devem permanecer. Uma entrada inválida encerra a execução; retome para preencher o item novamente. Cancelar durante as perguntas também não confirma um item incompleto.
7. **Deixar para depois:** pular o primeiro item e conferir o próximo. Retomar deve voltar ao primeiro ainda não conferido. Após chegar ao fim, os itens deixados para depois devem reaparecer.
8. **Revisão:** revisar um item já conferido e depois um não conferido. O primeiro não pode aumentar o contador ou criar outra chave para o mesmo ID; o segundo deve aumentar o contador uma vez. Os valores anteriores devem aparecer como padrões nas perguntas.
9. **Pausa e encerramento:** pausar e retomar; cancelar a confirmação de encerramento; encerrar com itens faltando e confirmar que o resultado fica marcado como FINALIZADA, com linhas não conferidas. Uma conferência finalizada deve recusar retomada/edição e permitir resumo.
10. **Backup:** fazer duas atualizações. Principal deve conter a mais recente e backup a imediatamente anterior. Conferir JSON e nomes/extensões reais: a conversão `files.convert` com `public.plain-text` deve produzir arquivos que `files.save` salva como `.json`/`.html`, sem extensão adicional.
11. **Interrupções:** encerrar a execução durante perguntas, durante a cópia de backup e durante a gravação principal. Verificar qual checkpoint permaneceu. Se o principal estiver corrompido, recuperar o backup em nova conferência e confirmar que o principal antigo não foi substituído.
12. **Conflito:** numa pasta de teste, alterar o principal entre leitura e salvamento. O hash deve detectar a diferença antes de substituir backup/principal. Isso não comprova atomicidade ou proteção contra gravações simultâneas durante a janela entre checagem e escrita.
13. **Histórico:** criar mais de cinco conferências, abrir as recentes e as anteriores. Confirmar que iniciar outra conferência preserva todos os arquivos das anteriores. Arquivos V3/V4 devem permanecer intocados nas pastas antigas.
14. **Resumo:** verificar as 60 linhas, estoque, Conferido?, comprar, processar e as três listas. Conferir acentos e caracteres especiais. Confirmar que o HTML abre visualmente em Quick Look, sem aparecer apenas como texto-fonte.
15. **Desempenho:** medir abertura, troca de item, salvamento e resumo no aparelho. Registrar modelo do iPhone e versão do iOS. O número de ações diminuiu, mas não há medição real de duração/memória.

As verificações estáticas e o compilador oficial não substituem esses testes. Não usar o resultado como único registro de produção antes da validação.

## Reteste prioritário da V5.1

- Importar a versão cujo nome é **PAPA PIZZA V5.1**.
- Selecionar uma pasta-base existente e vazia de teste no iCloud Drive; confirmar que foram criados PAPA PIZZA, V5 e as três subpastas, sem o erro do vídeo.
- Confirmar que depois da preparação abre o seletor de Papa_Pizza.json. Cancelar se ainda não quiser conferir itens.
- Executar novamente escolhendo exatamente a mesma base: a preparação deve reutilizar as pastas sem duplicá-las e permitir retomar os arquivos salvos nela.
- Se houver falha, usar Mostrar e registrar a ação destacada e a mensagem. O Build não substitui esse reteste.

## Reteste prioritário da V5.2

- Importar/assinar o projeto cujo nome é **PAPA PIZZA V5.2**, para distinguir dos atalhos antigos.
- Selecionar Atalhos como base e o mesmo JSON original; manter os arquivos existentes.
- Confirmar se a comparação dos 60 produtos avança até o menu Próximo item.
- Se houver mensagem Diagnostico do cadastro, registrar os valores entre colchetes: ID lido, nome lido e nome esperado. A mensagem não declara que o arquivo está incorreto; esses valores são necessários para isolar a causa.
- Não renomear produtos, apagar arquivos ou dispensar a validação para contornar o erro.

## Reteste prioritário da V5.3

- Instalar o projeto com o nome **PAPA PIZZA V5.3**, mantendo os arquivos anteriores.
- Selecionar a mesma pasta Atalhos e o mesmo JSON original. A leitura de Massa deve passar pela validação, sem trocar ou renomear esse produto.
- Confirmar se chega ao primeiro item alfabético e se consegue salvar, pausar e retomar um registro.
- Se a mensagem de comparação reaparecer, registrar a mensagem completa. Ainda não há confirmação de execução da V5.3 no aparelho.

## Reteste prioritário da V5.4 — pastas manuais e etapas

1. Preservar tudo que já existir. Preparar a árvore de PREPARAR_PASTAS.md, sem criar arquivos vazios.
2. Importar/assinar o projeto com o nome **PAPA PIZZA V5.4**. Selecionar **V5**, não Atalhos, no primeiro seletor; depois selecionar o JSON original.
3. Registrar se aparecem 1/3 Cadastro validado, 2/3 JSON preparado e 3/3 Arquivo inicial salvo e relido. Tocar OK em cada um.
4. Se ficar executando, informar o último número exibido, ou dizer que não apareceu nenhum. Ainda não há causa comprovada para a demora.
5. Se chegar ao menu, conferir um item com estoque zero, salvar, pausar e retomar. Verificar principal e backup antes de usar dados reais.

## Reteste prioritário da V5.5 — arquivo JSON real e referência

O vídeo da V5.4 chegou ao menu e às perguntas, mas mostrou Principal ausente no primeiro salvamento seguinte. O usuário informou arquivos TXT com a data ausente no nome. Não excluir nem renomear esses arquivos.

1. Importar/assinar **PAPA PIZZA V5.5** e escolher Nova conferência, usando a mesma pasta V5 e o cadastro original.
2. Confirmar os três avisos e verificar nome com data/hora e extensão JSON, não TXT.
3. Registrar um item com estoque zero e comprar/processar positivos. A atualização deve concluir, gerar backup e abrir o menu novamente.
4. Pausar, retomar, conferir as quantidades e revisar o mesmo ID sem duplicá-lo.
5. Gerar resumo e verificar a extensão HTML e abertura visual.
6. Se aparecer aviso de data ou extensão, registrar exatamente os valores exibidos. A correção ainda não foi homologada em aparelho.
