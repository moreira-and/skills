# CDC, Dedupe e SCD

Avalie uma operação de changes quando for necessário manter estado por chave, aplicar inserts/updates/deletes de uma fonte CDC ou manter histórico SCD. Os exemplos são ilustrativos; confirme sintaxe e disponibilidade na versão-alvo.

## Informações obrigatórias para a decisão

- Chave lógica, simples ou composta.
- Coluna/expressão de sequenciamento confiável para determinar a ordem por chave.
- Se o resultado mantém apenas estado atual (SCD tipo 1) ou histórico (SCD tipo 2).
- Condições de delete/truncate, se existirem, e colunas propagadas.
- Confirmação de que a semântica de entrada corresponde ao resultado solicitado.

Se a origem não garante sequência confiável, pare e peça decisão. Não invente uma ordem.

## Forma ilustrativa

```sql
CREATE OR REFRESH STREAMING TABLE sample_catalog.sample_schema.processed_record
CLUSTER BY (event_date)
COMMENT 'Estado atual dos registros processados por chave.';

APPLY CHANGES INTO sample_catalog.sample_schema.processed_record
FROM STREAM(sample_catalog.sample_schema.source_record)
KEYS (record_id)
SEQUENCE BY event_timestamp
STORED AS SCD TYPE 1;
```

Conforme a necessidade de negócio e a gramática da versão, cláusulas opcionais podem incluir condições de delete (`APPLY AS DELETE WHEN ...`), truncamento de histórico em SCD tipo 2 (`APPLY AS TRUNCATE WHEN ...`) e seleção/exclusão das colunas propagadas (`COLUMNS (...)` ou forma equivalente suportada). Confirmar disponibilidade e sintaxe exata no runtime-alvo antes de usar; não adicionar essas cláusulas por padrão.

## Restrições e cautelas

- O alvo deve seguir o tipo/gerenciamento exigido pelo pipeline; não misturar gravações manuais e gerenciamento de changes no mesmo alvo sem suporte explícito.
- O alvo é uma streaming table declarada separadamente e gerenciada pela operação de changes; o clustering, quando usado, fica na definição do alvo e não deve ser copiado para a cláusula de changes.
- Declare a estratégia SCD explicitamente para mostrar se o estado atual ou o histórico é necessário.
- `APPLY AS DELETE WHEN`, truncamento SCD2 e projeção `COLUMNS` são decisões com efeitos de negócio; documente as condições e revise exemplos por versão.
- Dedupe por `ROW_NUMBER`, `dropDuplicates`, `left_anti` e `MERGE` não são transformações universalmente intercambiáveis. `dropDuplicates` sozinho não garante selecionar o registro mais recente; um `orderBy` posterior tampouco garante essa semântica.
- Checkpoints não tornam toda estratégia de reprocessamento obsoleta. Avalie se uma janela de sobrescrita no legado tinha intenção de corrigir ou substituir dados históricos.

## Mapeamento conceitual

| Padrão legado | Possível destino | Condição para equivalência |
|---|---|---|
| `ROW_NUMBER()` por chave ordenado por evento e filtro do primeiro | Changes por chave ou query batch | Ordem total, empate resolvido e atualização incremental compatível |
| `MERGE` manual com upsert | Changes por chave | A operação e os deletes correspondem ao contrato da fonte |
| SCD tipo 2 | Changes com histórico | Vigência, colunas de controle e requisitos de retenção confirmados |

Não gere código de produção antes de resolver chave, sequência e eventuais diferenças semânticas.