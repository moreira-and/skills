# Tasks: Databricks Migration Specialist Agent

**Input**: Design documents from `/specs/002-databricks-migration-agent/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/skill-contract.md](./contracts/skill-contract.md), [quickstart.md](./quickstart.md)

**Tests**: Sem testes automatizados novos; a validação usa o validador estrutural existente e revisão semântica (constituição, princípio IV).

**Organization**: Tarefas agrupadas por user story. Todo o conteúdo é em português, como as skills irmãs. Regras técnicas são referenciadas por link, nunca copiadas.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup

- [x] T001 Ler [skills/pyspark-to-lakeflow/SKILL.md](../../skills/pyspark-to-lakeflow/SKILL.md), [skills/lakeflow-pipelines/SKILL.md](../../skills/lakeflow-pipelines/SKILL.md) e [skills/databricks-sql-quality/SKILL.md](../../skills/databricks-sql-quality/SKILL.md) para mapear regras a referenciar e evitar duplicação
- [x] T002 Criar o diretório `skills/databricks-migration-engineer/references/`

---

## Phase 2: Foundational

- [x] T003 Criar `skills/databricks-migration-engineer/SKILL.md` com frontmatter somente `name: databricks-migration-engineer` e `description` (30 a 1024 caracteres, com "Use when", entre aspas se houver pontuação YAML; deve citar migração para Databricks, conversão PySpark→Lakeflow, uso das regras locais e a postura de engenheiro de dados, terminando com "Use when …" e listando situações de ativação (inventariar, converter, validar e relatar migrações); não pode ficar genérica nem se sobrepor às descrições de `pyspark-to-lakeflow` e `lakeflow-pipelines`), mais título, persona de engenheiro de dados sênior, responsabilidade única e seção "Quando não usar" (FR-001, FR-011, contrato)

**Checkpoint**: a skill existe e valida estruturalmente.

---

## Phase 3: User Story 1 - Delegar uma migração ao agente (Priority: P1) 🎯 MVP

**Goal**: o agente inventaria, planeja e converte aplicando as regras locais por referência.

**Independent Test**: dado um job legado pequeno, o agente produz inventário, plano com regras citadas, artefatos convertidos e lista de itens não validados.

- [x] T004 [P] [US1] Criar `skills/databricks-migration-engineer/references/workflow.md` com as cinco etapas (inventariar, planejar, converter, validar, relatar), critério de saída de cada uma e tratamento de informação faltante: perguntar chave, ordenação, latência, responsável e ambiente em vez de supor (FR-004, FR-008)
- [x] T005 [US1] Em `skills/databricks-migration-engineer/SKILL.md`, adicionar o fluxo obrigatório resumido com link para `references/workflow.md` e referências pelo nome (sem links `../`, rejeitados pelo validador) a `pyspark-to-lakeflow`, `lakeflow-pipelines` e `databricks-sql-quality`, indicando quando cada uma se aplica; regra local prevalece e divergência é registrada; versão ou sintaxe não confirmada é marcada "não validada" (FR-002, FR-003, FR-006)
- [x] T006 [US1] Em `skills/databricks-migration-engineer/references/workflow.md`, cobrir fontes não PySpark, regras locais silenciosas ou conflitantes e ausência de acesso ao workspace, conforme Edge Cases da spec

**Checkpoint**: US1 utilizável sozinha.

---

## Phase 4: User Story 2 - Instrução em massa (Priority: P1)

**Goal**: resultados consistentes em muitas tarefas e lotes.

**Independent Test**: três cargas diferentes geram a mesma estrutura de entregas e citam as regras.

- [x] T007 [P] [US2] Criar `skills/databricks-migration-engineer/references/report-template.md` com as seções: escopo, inventário, regras aplicadas (com link), divergências, premissas, itens não validados, riscos residuais, pendências do lote (FR-005)
- [x] T008 [US2] Em `skills/databricks-migration-engineer/references/workflow.md`, adicionar a regra de divisão de cargas grandes em lotes revisáveis, com relato de progresso e itens restantes (FR-010)
- [x] T009 [US2] Em `skills/databricks-migration-engineer/SKILL.md`, adicionar "Formato de saída" com link para `references/report-template.md` e a regra de recusar ou redirecionar pedidos fora de migração Databricks e engenharia de dados (FR-005, FR-011)

---

## Phase 5: User Story 3 - Comportamento seguro e revisável (Priority: P2)

**Goal**: limites explícitos de ação no Genie Code.

**Independent Test**: pedidos de deploy, commit/push, produção ou exposição de segredos são recusados; relatórios separam validação estática de real.

- [x] T010 [P] [US3] Criar `skills/databricks-migration-engineer/references/guardrails.md` com: nunca fazer deploy, commit ou push nem agir em produção; leitura e validação só no workspace de teste; confirmação explícita antes de ação destrutiva ou irreversível; nunca expor segredos ou dados sensíveis; separar validação estática de execução real e não declarar a segunda sem tê-la feito (FR-007, FR-009)
- [x] T011 [US3] Em `skills/databricks-migration-engineer/SKILL.md`, adicionar "Limites obrigatórios" resumidos com link para `references/guardrails.md`, distinguindo obrigatório de recomendação

---

## Phase 6: User Story 4 - Definição mantível e descobrível (Priority: P3)

**Goal**: o agente é documentado e passa na validação do catálogo.

**Independent Test**: um mantenedor encontra o agente no README e o validador passa sem erros.

- [x] T012 [US4] Atualizar `README.md`: incluir a skill no catálogo (hoje descrito com três capacidades), seu propósito, limites, relação com as skills de regras e a nota de que no Genie Code as quatro skills devem ficar lado a lado em `Workspace/.assistant/skills/`, que invocação e permissões dependem do consumidor e que as restrições são instruções, não controle técnico (FR-013, FR-014, FR-015)
- [x] T013 [US4] Executar `uv run --locked python scripts/validate_skills.py`, `uv run --locked python -m unittest discover -s tests -v` e `uv run --locked pre-commit run --all-files`; corrigir qualquer erro nos arquivos novos (FR-013, SC-006)

---

## Phase 7: Polish & Cross-Cutting

- [x] T014 Revisão semântica conforme [quickstart.md](./quickstart.md) e [contrato](./contracts/skill-contract.md): ativação e não ativação, nenhuma regra técnica duplicada das skills irmãs, sem contradições, links resolvem, `SKILL.md` com no máximo 100 linhas (as skills irmãs têm 30 a 36), com detalhes só em `references/` e cada referência linkada diretamente do `SKILL.md` (FR-012) (SC-002, SC-006)
- [x] T015 Criar `specs/002-databricks-migration-agent/checklists/outcomes-review.md` mapeando SC-001 a SC-005 aos cenários 2 a 5 do [quickstart.md](./quickstart.md): amostra de 5 pedidos, critério de aprovação e campo de resultado observado, todos desmarcados até a execução manual no workspace de teste (SC-001, SC-002, SC-003, SC-004, SC-005)
- [x] T016 Registrar em `specs/002-databricks-migration-agent/quickstart.md` que os cenários no Genie Code (passos 1 a 5) permanecem pendentes de execução manual no workspace de teste, sem declarar validação real

---

## Dependencies & Execution Order

- Setup (T001-T002) → Foundational (T003) → US1, US2, US3 → US4 → Polish.
- US1, US2 e US3 só compartilham `SKILL.md` e `workflow.md`; arquivos novos separados são paralelizáveis, edições do mesmo arquivo são sequenciais (T003 → T005 → T009 → T011; T004 → T006 → T008).
- T012 depende da skill completa; T013 depende de T012.

## Parallel Opportunities

- T004, T007 e T010 (arquivos de referência distintos) após T003.

## Implementation Strategy

- **MVP**: T001-T006 (US1), já com skill válida e fluxo.
- Depois US2 e US3 (P1/P2), em seguida README e validação (US4) e revisão final.

## Phase 8: Convergence

- [x] T017 Executar `uv run --locked pre-commit run --all-files` (mdformat, codespell, ruff) em `README.md` e `skills/databricks-migration-engineer/`, em ambiente com `uv` e `uv.lock`, e corrigir qualquer formatação ou erro; o T013 foi marcado como feito sem esses hooks terem rodado (apenas o validador e os testes) per FR-013 / SC-006 (partial)
