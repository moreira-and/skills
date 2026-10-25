# Implementation Plan: Databricks Migration Specialist Agent

**Branch**: `002-databricks-migration-agent` | **Date**: 2026-10-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-databricks-migration-agent/spec.md`

## Summary

Entregar o "agente" como uma skill do catálogo, `skills/databricks-migration-engineer/`, no padrão Agent Skills. O Genie Code do Databricks carrega skills nesse padrão a partir de `.assistant/skills/` e não tem um formato separado de agente. A skill define a persona de engenheiro de dados sênior, o fluxo fixo (inventariar, planejar, converter, validar, relatar), os limites de segurança e o formato do relatório. As regras técnicas são delegadas, por referência de nome, às três skills existentes, sem cópia de conteúdo.

## Technical Context

**Language/Version**: Markdown com frontmatter YAML (Agent Skills); validador em Python 3 stdlib já existente

**Primary Dependencies**: skills irmãs `databricks-sql-quality`, `lakeflow-pipelines`, `pyspark-to-lakeflow`; nenhuma dependência nova

**Storage**: arquivos no repositório

**Testing**: `scripts/validate_skills.py` e `python -m unittest` (via uv); revisão semântica manual; cenários de [quickstart.md](./quickstart.md)

**Target Platform**: Genie Code (Databricks), workspace de teste; skill de workspace em `Workspace/.assistant/skills/`

**Project Type**: catálogo de skills (documentação de instruções)

**Performance Goals**: N/A

**Constraints**: `name` igual ao diretório; descrição com "Use when" e mais de 30 caracteres; `SKILL.md` curto, com detalhes em `references/`; sem campos de frontmatter customizados; sem deploy, commit ou push; o Genie Code só acessa o workspace de teste

**Scale/Scope**: 1 skill com 3 referências; sem scripts

## Constitution Check

| Princípio | Avaliação |
|---|---|
| I. Interoperabilidade | Passa. Usa só `name` e `description` do padrão. Que o Genie Code carrega skills em `.assistant/skills/` vem da documentação oficial; invocação por `@` e permissões são limites do consumidor, documentados no README. |
| II. Uma responsabilidade | Passa. A responsabilidade é orquestrar a migração (postura, fluxo, limites, relatório), delegando regras técnicas às skills irmãs. |
| III. Execução segura | Passa. Sem scripts. Proíbe deploy, commit/push e produção, exige confirmação para ações destrutivas e proíbe expor segredos. |
| IV. Validação não basta | Passa. O plano inclui revisão semântica de ativação, contradições e redundância com as skills irmãs. |
| V. Evolução rastreável | Passa. Mudança material feita pelo ciclo Spec Kit; sem artefatos de preenchimento. |

Sem violações. Reavaliação pós-design: sem mudança.

## Project Structure

### Documentation (this feature)

```text
specs/002-databricks-migration-agent/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── skill-contract.md
├── checklists/
└── tasks.md             # /speckit-tasks
```

### Source Code (repository root)

```text
skills/databricks-migration-engineer/
├── SKILL.md                      # persona, escopo, fluxo, limites (curto)
└── references/
    ├── workflow.md               # etapas, lotes e critérios de saída
    ├── guardrails.md             # segurança e limites do Genie Code
    └── report-template.md        # estrutura padrão do relatório
README.md                         # entrada do catálogo e limites do consumidor
```

**Structure Decision**: uma skill de orquestração no catálogo `skills/`, irmã das skills de regras. As skills de regras são citadas pelo nome, não por link `../` (rejeitado pelo validador), e devem ficar lado a lado em `.assistant/skills/`.

## Complexity Tracking

Sem violações a justificar.
