# Modelo de conteúdo

Sem dados persistidos em runtime; são entidades documentais.

## Skill do agente

- **Identidade**: `databricks-migration-engineer` (nome igual ao diretório).
- **Campos**: `name`, `description` (capacidade e "Use when", entre 30 e 1024 caracteres).
- **Corpo**: persona, responsabilidade, quando não usar, fluxo, limites, links para referências e skills irmãs.

## Referência de fluxo

Etapas inventariar, planejar, converter, validar e relatar, cada uma com critério de saída, e regra de divisão em lotes (FR-004, FR-010).

## Referência de limites

Proibições (deploy, commit/push, produção, segredos), confirmações exigidas, validação estática versus real e tratamento de informação faltante (FR-007 a FR-009, FR-015).

## Modelo de relatório

Seções: escopo, inventário, regras aplicadas (com link), divergências, premissas, itens não validados, riscos residuais, pendências do lote (FR-005).

## Relações

A skill do agente referencia `databricks-sql-quality`, `lakeflow-pipelines` e `pyspark-to-lakeflow`. Estas não referenciam o agente, então não há ciclo.
