# Mapa de Conteúdo Legado

Este mapa registra destino planejado para cada fonte lida. Foram conferidos os 22 arquivos de `legado/`; todos têm entrada abaixo. `legado/` é mantido intacto como entrada e evidência de proveniência. Destinos indicam o desenho inicial de três capacidades, sujeito à revisão semântica antes da publicação.

| Fonte | Conteúdo / decisão de destino |
|---|---|
| `legado/SKILL.md` | Raiz da capacidade `databricks-sql-quality`; reescrever fluxo e metadados conforme o contrato portátil. Não prometer `dbsql_linter.py`, auto-fix ou etapas sem ferramenta fornecida. |
| `legado/SKILL (2).md` | Raiz da capacidade `lakeflow-pipelines`; instruções essenciais de autoria, revisão, ativação, limitações e referências. Remover dependências locais não incluídas como pré-requisitos obrigatórios. |
| `legado/SKILL (3).md` | Raiz da capacidade `pyspark-to-lakeflow`; preservar inventário, fases, gates de aprovação, rastreabilidade e entrega. Referenciar as outras skills apenas como orientação complementar. |
| `legado/apply-changes-cdc.md` | Referência de Lakeflow para CDC, dedupe e SCD; preservar requisitos de chave, sequência e confirmação de semântica/versionamento. |
| `legado/column-naming.md` | Referência DBSQL canônica para prefixos e decisões de nomes. Conservar como convenção organizacional, não padrão universal. |
| `legado/conversion-patterns.md` | Referência de migração para conversões e exemplos; incluir ressalvas de semântica de null, desempates, casts e equivalência. |
| `legado/dabs-template.md` | Referência de migração com exemplos condicionais; marcar campos, ambientes e configurações que dependem de workspace/versão. |
| `legado/data-quality-expectations.md` | Referência de Lakeflow para expectativas, severidades e efeitos; verificar sintaxe antes de declarar compatibilidade. |
| `legado/deployment-execution.md` | Referência de Lakeflow sobre ciclo de vida, execução e monitoramento; exemplos devem destacar dependências do ambiente. |
| `legado/explicit-typing.md` | Referência DBSQL para convenção local de declaração de tipos. |
| `legado/materialized-views.md` | Referência Lakeflow para escolha de materialized view e risco de recomputação. |
| `legado/medallion-architecture.md` | Referência Lakeflow sobre camadas e grafo declarativo; apresentar organização como orientação contextual. |
| `legado/metadata-documentation.md` | Referência DBSQL para convenção local de `COMMENT`, incluindo critérios organizacionais. |
| `legado/python-vs-sql.md` | Referência Lakeflow para escolha de linguagem e cautela com API Python/versionamento; consolidar com o arquivo duplicado. |
| `legado/python-vs-sql (1).md` | Duplicata byte a byte confirmada de `python-vs-sql.md` (SHA-256 `2da5abd9ba0c971b300a5f7da5ec6e79067f2d9a3a73b37c399a059605ced291`); publicar uma única referência e manter os dois originais intactos. |
| `legado/sql-readability.md` | Referência DBSQL para estilo e estrutura; explicitar que regras são política local, não exigência universal do produto. |
| `legado/streaming-tables.md` | Referência Lakeflow para incrementalidade, append-only e mudanças de schema; verificar afirmações dependentes de versão. |
| `legado/table-naming.md` | Referência DBSQL para convenções locais de nome de objetos. |
| `legado/validation-checklist.md` | Referência de migração para rastreabilidade, revisão de lógica, consistência dos artefatos e manifesto final. |
| `legado/validate_pipeline_syntax.py` | Candidato a `skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py`; manter como verificação heurística, cobrir erros/avisos/entradas inválidas e documentar limitações. |
| `legado/openai.yaml` | Metadata específico de consumidor; não copiar para o frontmatter portátil. Reaproveitar apenas texto de ativação útil na descrição. Confirmar referências de assets não inventariadas antes de qualquer adaptação de consumidor. |
| `legado/openai (1).yaml` | Mesmo tratamento; comparar se necessário, não publicar como skill interoperável nem depender dos assets. |

## Conflitos e dependências sem fonte local

- `python-vs-sql` menciona `nm_` como prefixo aplicável, enquanto `column-naming.md` declara `nm_` descontinuado. `column-naming.md` é a lista canônica; a referência consolidada não repetirá a menção obsoleta e os originais permanecem inalterados.
- Os dois arquivos `python-vs-sql` foram comparados byte a byte e são idênticos; não há diferença de conteúdo a preservar separadamente.
- `dbsql_linter.py`, `naming-governance.md`, `audit-columns.md`, imagens dos YAMLs e skills externas mencionadas não foram fornecidos; não os apresentar como disponíveis no catálogo.
- Conversões de CDC/dedupe, `REPLACE WHERE`, APIs Python, expectativas, streaming, materialized views e DAB precisam preservar as ressalvas de semântica e compatibilidade por versão identificadas na pesquisa.

## Evidência de versão Databricks

Não foi especificado workspace nem versão Databricks alvo, e nenhum deploy foi executado. As afirmações e exemplos dependentes de produto abaixo permanecem **não validados** para compatibilidade de runtime; as referências instruem confirmar documentação oficial antes de uso operacional.

| Artefato | Status | Motivo |
|---|---|---|
| `skills/lakeflow-pipelines/references/streaming-tables.md` | Não validado para versão | Sem runtime ou versão-alvo |
| `skills/lakeflow-pipelines/references/materialized-views.md` | Não validado para versão | Incrementalidade e suporte podem variar por query/versão |
| `skills/lakeflow-pipelines/references/apply-changes-cdc.md` | Não validado para versão | Gramática e capacidades de CDC dependem da versão |
| `skills/lakeflow-pipelines/references/data-quality-expectations.md` | Não validado para versão | Sintaxe/efeitos precisam ser confirmados no alvo |
| `skills/lakeflow-pipelines/references/medallion-architecture.md` | Não validado para versão | Flows e organização de múltiplas fontes dependem da API vigente |
| `skills/lakeflow-pipelines/references/python-vs-sql.md` | Não validado para versão | API Python não foi vinculada a um runtime alvo |
| `skills/lakeflow-pipelines/references/deployment-execution.md` | Não validado para workspace/versão | Configuração, monitoramento e recursos dependem do ambiente |
| `skills/pyspark-to-lakeflow/references/conversion-patterns.md` | Não validado para dialeto/runtime | Equivalências SQL precisam ser verificadas no destino |
| `skills/pyspark-to-lakeflow/references/dabs-template.md` | Não validado para CLI/workspace | Schema e campos do bundle precisam ser validados no ambiente |
| `skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py` | Heurísticas testadas localmente; não certifica runtime | O script usa regex e não faz deploy nem análise completa de dialeto |