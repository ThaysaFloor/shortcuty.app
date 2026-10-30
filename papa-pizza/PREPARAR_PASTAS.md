# Preparar as pastas para a V5.4

No app **Arquivos**, entre em **iCloud Drive → Atalhos** e confira esta estrutura:

```text
Atalhos/
  Papa_Pizza.json
  PAPA PIZZA/
    V5/
      Conferencias/
      Backups/
      Resumos/
```

Crie somente as pastas que faltarem. Se já existirem, preserve todo o conteúdo. Use os nomes exatamente como acima: `PAPA PIZZA` tem espaço e `Conferencias` não tem acento.

**O JSON original é o único arquivo necessário para começar.** Não é preciso criar arquivo vazio de conferência, backup, índice, configuração, planilha ou HTML. O atalho gera esses registros e resumos durante o uso.

Se você já tem o JSON em Atalhos, mantenha-o ali. Uma cópia intacta do arquivo recebido também está disponível em [Papa_Pizza.json](Papa_Pizza.json); não substitua seu arquivo sem necessidade.

## No atalho

1. Importe e assine a versão com o nome **PAPA PIZZA V5.4**.
2. Escolha Nova conferência.
3. No seletor de pastas, abra `Atalhos → PAPA PIZZA → V5` e toque **Abrir** para selecionar a pasta **V5**.
4. Quando solicitar o cadastro, volte à pasta Atalhos e selecione `Papa_Pizza.json`.
5. Para este teste, acompanhe os três avisos temporários: **1/3 Cadastro validado**, **2/3 JSON preparado** e **3/3 Arquivo inicial salvo e relido**. Toque OK em cada um.

Nas próximas execuções, selecione a mesma pasta V5. O código abre as subpastas existentes; não tenta criá-las. Se faltar uma delas, o iOS poderá mostrar erro de localização antes de abrir o cadastro.

Se o atalho continuar executando sem perguntas, informe o último número exibido, ou diga que nenhum dos três apareceu. Preparar as pastas elimina essa parte da configuração; ainda é necessário localizar a demora observada depois de ler o JSON.
