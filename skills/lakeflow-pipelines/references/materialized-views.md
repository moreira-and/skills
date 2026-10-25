# Materialized Views

## Quando considerar

Considere materialized view quando a origem é uma tabela batch, quando a transformação precisa refletir recomputação sobre o conjunto completo ou quando a lógica depende do histórico inteiro, como certas windows, agregações completas ou joins com fan-out. Para leitura leve sem materialização, considere uma view comum.

Exemplo conceitual:

```sql
CREATE OR REFRESH MATERIALIZED VIEW sample_catalog.sample_schema.daily_metric
COMMENT 'Agregação de métricas por dimensão de negócio.'
AS SELECT
    category,
    COUNT(*) AS event_count,
    SUM(amount) AS total_amount
FROM sample_catalog.sample_schema.processed_record
GROUP BY category;
```

## Custo e incrementalidade

- O mecanismo pode atualizar incrementalmente quando a query e suas fontes permitem.
- Se a query não for incrementalizável, a atualização pode recomputar o conjunto completo e aumentar custo/tempo.
- Antes de sugerir materialized view pesada, explique o risco e confirme o requisito de atualização com a pessoa usuária.
- Dedupe por chave com evento ordenável pode se encaixar melhor em um fluxo de CDC, mas não converter sem verificar semântica, chave e sequência.
- Materialized view materializa resultado e ocupa armazenamento; view comum é definição lógica avaliada na leitura. Confirmar comportamento vigente da plataforma.
- Clustering, comentários e regras de qualidade podem estar disponíveis para o objeto, mas a combinação e a sintaxe suportadas precisam ser confirmadas na versão-alvo.

## Regra prática

| Necessidade | Opção a avaliar |
|---|---|
| Fonte incremental e transformação que não exige histórico completo | Streaming table |
| Upsert, delete, SCD ou dedupe por chave | Streaming table com operação de changes apropriada |
| Recomputação/consulta sobre o conjunto batch completo | Materialized view |
| Camada lógica leve sem necessidade de materialização | View |

Os nomes de objetos, refresh e suportes de cláusula nos exemplos dependem da versão Lakeflow usada.