# Padrões de Conversão PySpark para SQL Declarativo

Use esta tabela como ponto de partida, nunca como prova automática de equivalência. Verifique semântica de nulos, tipos, timezone, ordenação, empates, duplicatas e incrementalidade para cada transformação. Funções e sintaxe devem ser confirmadas na versão SQL de destino.

## Leitura e expressões

| PySpark | Possível forma SQL | Cautela |
|---|---|---|
| `spark.read.parquet(path)` | `read_files(path, format => 'parquet')` | Batch e acesso ao storage devem estar configurados |
| Leitura incremental de Parquet | `STREAM read_files(...)` | Confirmar fonte, permissões e suporte incremental |
| `spark.table(name)` | `catalog.schema.table` | Confirmar publicação e catálogo da tabela |
| `F.col('c')` | `c` | Qualificar quando houver múltiplas fontes |
| `F.lit(v)` | literal SQL ou `CAST(v AS tipo)` | Tipagem e escape explícitos |
| `when(...).otherwise(...)` | `CASE WHEN ... THEN ... ELSE ... END` | Preservar ordem e ramo default |
| `.cast(type)` | `CAST(expr AS TYPE)` | Comparar coerção/overflow e valores inválidos |
| `to_timestamp`, `to_date` | `TO_TIMESTAMP`, `TO_DATE` | Formato e timezone influenciam resultado |
| `date_format` | `DATE_FORMAT` | Máscara deve corresponder à semântica desejada |
| `regexp_replace`, `regexp_extract` | Função de mesmo nome | Confirmar regras de regex/índice |
| `trim`, `lower`, `upper`, `coalesce` | Função SQL de mesmo nome | Verificar collation e comportamento de NULL |
| `concat`, `concat_ws`, `substring`, `length`, `split` | Função SQL de mesmo nome | Verificar tipos, posição e separador |
| `explode`, `array`, `struct`, `size` | Função SQL equivalente | Revisar cardinalidade e schema complexo |

## Agregação, hashing e windows

| PySpark | Possível forma SQL | Cautela |
|---|---|---|
| `count`, `countDistinct` | `COUNT`, `COUNT(DISTINCT ...)` | Nulos e cardinalidade |
| `sum`, `avg`, `min`, `max` | Funções SQL correspondentes | Precisão e tipo resultante |
| `min_by`, `max_by` | `MIN_BY`, `MAX_BY` | Empates na chave de ordenação |
| `first`, `last`, `collect_set`, `collect_list` | Agregações SQL correspondentes | Ordem e determinismo podem diferir |
| Soma de `when(cond, 1)` | `COUNT_IF(cond)` ou `SUM(CASE...)` | Verificar contagem de NULL |
| `md5`/`sha2` de concatenação | `MD5`/`SHA2` com expressão equivalente | Separador, encoding e NULL alteram hash |
| `monotonically_increasing_id()` | Sem equivalente direto garantido | UUID/ROW_NUMBER também alteram identidade/determinismo; aprovar desenho |
| `row_number` por chave/ordem | `ROW_NUMBER() OVER (...)` | Definir desempate para ordem total |
| `lag`, `lead`, `first`, `last` em window | Funções window SQL | Preservar frame, ordem e partição |
| Filtrar `row_number = 1` | `QUALIFY ROW_NUMBER() ... = 1` | `QUALIFY` é sintaxe dependente de dialeto e a dedupe não implica CDC |

## Deduplicação e escrita

| Padrão PySpark | Opção declarativa a avaliar | Cautela |
|---|---|---|
| `dropDuplicates(keys)` | Changes por chave ou dedupe batch | Não escolhe necessariamente o evento mais recente |
| `row_number` ordenado e filtro primeiro | Changes ou query batch com `QUALIFY` | Empates e incrementalidade precisam ser resolvidos |
| `left_anti` para inserir só novos | Changes por chave ou anti-join SQL | Não equivaler automaticamente a SCD1 |
| `MERGE INTO` | Operação declarativa de changes | Conferir updates/deletes e sequência |
| `write append` | Streaming table / fluxo append | Confirmar append-only e grafo |
| `write overwrite` | Refresh/materialização apropriada | Semântica de substituição precisa ser preservada |
| `replaceWhere` | Estratégia declarativa de refresh/reprocessamento | Pode representar correção histórica; não presumir que checkpoint substitui sua intenção |

## Dados estáticos e nulos

- Converter `None` para `NULL`, booleanos Python para `TRUE`/`FALSE` e escapar apóstrofos em strings.
- Declarar tipos conforme o contrato de schema e os requisitos do consumidor; não depender de inferência acidental de `VALUES`.
- Para dados inline, conferir a contagem, a ordem das colunas, valores nulos e literais antes/depois.
- Normalização de strings vazias, `null`, `none`, `nan` e variantes de caixa/whitespace deve preservar exatamente os padrões originais; SQL `IN` pode ser sensível a caixa se não normalizar.
- `na.fill` e `na.drop` podem ser expressos com `COALESCE`, `WHERE` ou regras de qualidade apenas se o efeito sobre linhas e colunas for o mesmo.

## Joins

| PySpark | Possível forma SQL | Cautela |
|---|---|---|
| `inner`, `left` | `INNER JOIN`, `LEFT JOIN` | Verificar duplicação e nulidade da chave |
| `left_anti` | `NOT EXISTS` ou anti-join equivalente | Semântica de NULL precisa ser comparada |
| `left_semi` | `EXISTS` | Evitar multiplicar linhas da esquerda |
| `crossJoin` | `CROSS JOIN` | Confirmar cardinalidade e custo |

## Procedimento de equivalência

1. Relacionar regra de negócio original ao trecho convertido.
2. Verificar tipos, precisão, nulos, timezone, ordem, empates e cardinalidade.
3. Conferir origem, destino e comportamento incremental/reprocessamento.
4. Registrar diferenças semânticas como decisão e obter aprovação antes de alterar comportamento.
5. Não preencher código de produção com TODO, reticências ou placeholders.

Ao nomear os objetos e campos convertidos, use substantivos principais no singular em catálogo, schema, tabela e coluna. Preserve nomes plurais quando forem parte obrigatória de uma API, configuração ou identificador externo; não reescreva chaves de sintaxe da plataforma.