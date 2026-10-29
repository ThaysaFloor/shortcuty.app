# Validação obrigatória no iPhone

Nenhum teste deste roteiro foi executado neste trabalho. Use dados descartáveis, mantenha cópias do cadastro e dos históricos e confirme a pasta do iCloud antes de começar.

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
