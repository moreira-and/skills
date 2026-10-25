# Contrato da skill `databricks-migration-engineer`

## Frontmatter

- `name: databricks-migration-engineer`, igual ao diretório.
- `description`: capacidade e frase "Use when", de 30 a 1024 caracteres.
- Nenhum outro campo.

## Corpo de `SKILL.md`

1. Persona de engenheiro de dados sênior e responsabilidade única.
2. Quando não usar.
3. Fluxo obrigatório de cinco etapas, com link para `references/workflow.md`.
4. Limites obrigatórios, com link para `references/guardrails.md`.
5. Formato de saída, com link para `references/report-template.md`.
6. Referência às skills de regras pelo nome (`databricks-sql-quality`, `lakeflow-pipelines`, `pyspark-to-lakeflow`), sem links `../`, que o validador do catálogo rejeita (links com no máximo um nível de profundidade).

## Invariantes

- Regras locais prevalecem; divergências são registradas.
- Não duplica o conteúdo técnico das skills irmãs.
- Não faz deploy, commit/push nem age em produção.
- Não afirma validação real sem execução no workspace de teste.
- Distingue obrigatório de recomendação.
