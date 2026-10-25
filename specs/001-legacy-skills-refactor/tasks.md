---
description: "Lista de tarefas da refatoração das skills legadas"
---

# Tasks: Refatoração das Skills Legadas

**Input**: Documentos de desenho em `specs/001-legacy-skills-refactor/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `legacy-content-map.md` e `quickstart.md`

**Tests**: Tarefas de teste incluídas para o validador de pipeline porque a constituição exige testes relevantes e o plano altera o contrato de erro/código de saída da ferramenta. Não é exigido fluxo TDD.

**Organization**: Tarefas agrupadas pelas histórias da especificação. Arquivos de `legado/` são fontes e não devem ser alterados ou removidos.

## Phase 1: Setup

**Purpose**: Preparar as pastas para as três capacidades aprovadas no desenho.

- [x] T001 Criar as pastas `skills/databricks-sql-quality/references/`, `skills/lakeflow-pipelines/references/`, `skills/lakeflow-pipelines/scripts/` e `skills/pyspark-to-lakeflow/references/` conforme `specs/001-legacy-skills-refactor/plan.md`

## Phase 2: Foundational

**Purpose**: Confirmar proveniência e resolver a base de conteúdo que todas as histórias utilizam.

- [x] T002 Comparar todos os 22 arquivos de `legado/`, confirmar igualdade da duplicata `python-vs-sql.md` e `python-vs-sql (1).md`, atualizar destinos/diferenças em `specs/001-legacy-skills-refactor/legacy-content-map.md` e registrar para aprovação qualquer exclusão ou mudança semântica proposta antes de aplicá-la

**Checkpoint**: Inventário conferido; nenhuma regra ou diferença relevante é descartada silenciosamente. As fontes em `legado/` continuam intactas.

## Phase 3: User Story 1 - Encontrar a orientação correta (Priority: P1)

**Goal**: Publicar três entradas autônomas com responsabilidades, limites e ativação distinguíveis.

**Independent Test**: Apresentar solicitações representativas de qualidade DBSQL, autoria/operação Lakeflow e migração PySpark; cada pessoa revisora escolhe uma capacidade principal e identifica quando não usá-la sem precisar carregar outra skill.

### Implementation for User Story 1

- [x] T003 [P] [US1] Criar `skills/databricks-sql-quality/SKILL.md` com responsabilidade de convenções/revisão DBSQL, limites explícitos, passos essenciais e descrição de ativação contendo literalmente `Use when`
- [x] T004 [P] [US1] Criar `skills/lakeflow-pipelines/SKILL.md` com responsabilidade de autoria/operação de pipelines, limites explícitos, passos essenciais e descrição de ativação contendo literalmente `Use when`
- [x] T005 [P] [US1] Criar `skills/pyspark-to-lakeflow/SKILL.md` com responsabilidade de processo de migração, limites explícitos, gates essenciais e descrição de ativação contendo literalmente `Use when`
- [x] T006 [US1] Atualizar `README.md` para remover a afirmação de catálogo sem skills e descrever as três capacidades portáteis, a ativação e a distinção entre catálogo `skills/` e comandos `.github/skills/`

**Checkpoint**: As três skills podem ser selecionadas por escopo e descrição, sem duplicar as regras detalhadas que serão documentadas em referências.

## Phase 4: User Story 2 - Migrar sem perder valor de negócio (Priority: P1)

**Goal**: Preservar as regras, exemplos, decisões e salvaguardas úteis em fontes canônicas organizadas por responsabilidade.

**Independent Test**: Conferir o mapa de conteúdo com as referências resultantes; cada regra considerada útil, gate, alerta operacional e exemplo tem destino verificável, duplicatas estão consolidadas e nenhuma equivalência semântica é tratada como automática sem suas ressalvas.

### Referências de qualidade DBSQL

- [x] T007 [P] [US2] Consolidar regras e exemplos de nomes de tabelas/views, qualificadores proibidos, exceções e critérios de pendência em `skills/databricks-sql-quality/references/table-naming.md`
- [x] T008 [P] [US2] Consolidar prefixos permitidos, árvore de decisão, proibições e exemplos de colunas em `skills/databricks-sql-quality/references/column-naming.md`; tratar `nm_` como descontinuado conforme a fonte canônica
- [x] T009 [P] [US2] Preservar a exigência organizacional de contrato de tipos visível e os exemplos válidos/inválidos em `skills/databricks-sql-quality/references/explicit-typing.md`
- [x] T010 [P] [US2] Preservar critérios de comentários de tabela/coluna, significado de negócio, unidades e exceções em `skills/databricks-sql-quality/references/metadata-documentation.md`, identificando-os como política local
- [x] T011 [P] [US2] Consolidar formatação, SELECT, CTEs, joins, aliases, windows, UNION e comentários em `skills/databricks-sql-quality/references/sql-readability.md`, identificando exceções como convenções locais

### Referências de autoria e operação Lakeflow

- [x] T012 [P] [US2] Preservar decisão entre streaming table e materialized view, incrementalidade, fontes append-only e riscos de schema evolution em `skills/lakeflow-pipelines/references/streaming-tables.md`, marcando detalhes dependentes de versão
- [x] T013 [P] [US2] Preservar critérios de materialização, recomputação e trade-offs de custo em `skills/lakeflow-pipelines/references/materialized-views.md`
- [x] T014 [P] [US2] Preservar requisitos de chave, sequência, SCD, deletes, truncates e limites de `APPLY CHANGES INTO` em `skills/lakeflow-pipelines/references/apply-changes-cdc.md`; alertar que dedupe e CDC exigem equivalência semântica
- [x] T015 [P] [US2] Preservar severidades e efeitos de `EXPECT`, `DROP ROW` e `FAIL UPDATE` em `skills/lakeflow-pipelines/references/data-quality-expectations.md`, com ressalva de sintaxe por versão
- [x] T016 [P] [US2] Preservar bronze/silver/gold, grafo declarativo, objetos independentes e múltiplas fontes em `skills/lakeflow-pipelines/references/medallion-architecture.md`, separando recomendações de regras obrigatórias
- [x] T017 [P] [US2] Consolidar `python-vs-sql.md` e `python-vs-sql (1).md` uma única vez em `skills/lakeflow-pipelines/references/python-vs-sql.md`, mantendo a cautela de confirmar API Python da versão-alvo
- [x] T018 [P] [US2] Preservar modos de execução, bundle/job, monitoramento e avisos de produção em `skills/lakeflow-pipelines/references/deployment-execution.md`, deixando valores de ambiente como exemplos configuráveis

### Referências do processo de migração

- [x] T019 [P] [US2] Consolidar padrões de conversão PySpark→SQL em `skills/pyspark-to-lakeflow/references/conversion-patterns.md`, mantendo ressalvas para NULL, desempates, casts, joins, hashing e incrementalidade
- [x] T020 [P] [US2] Adaptar os templates de bundle/job como exemplos não universais em `skills/pyspark-to-lakeflow/references/dabs-template.md`, identificando configurações dependentes de workspace e versão
- [x] T021 [P] [US2] Preservar checklist de consistência, lógica de negócio, completude e manifesto de entrega em `skills/pyspark-to-lakeflow/references/validation-checklist.md`

### Integração das referências e ferramenta

- [x] T022 [US2] Adicionar links relativos para as referências locais existentes nos três entrypoints `skills/databricks-sql-quality/SKILL.md`, `skills/lakeflow-pipelines/SKILL.md` e `skills/pyspark-to-lakeflow/SKILL.md`; não criar links que escapem da pasta da skill nem dependências obrigatórias entre capacidades
- [x] T023 [P] [US2] Migrar `legado/validate_pipeline_syntax.py` para `skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py`, preservar regras suportadas como heurísticas e retornar erro não zero para caminhos inexistentes ou diretórios fornecidos como arquivo

**Checkpoint**: Regras e ferramentas úteis estão na capacidade correta; o mapa aponta suas origens; conteúdos dependentes de ambiente/versão e dependências inexistentes não são anunciados como universais ou disponíveis.

## Phase 5: User Story 3 - Revisar e evoluir o catálogo (Priority: P2)

**Goal**: Demonstrar conformidade estrutural e semântica, documentação de ferramentas e limites claros de validação.

**Independent Test**: O validador do catálogo aceita as skills e referências; os testes da ferramenta cobrem achados e erros de entrada; a revisão humana não encontra responsabilidade ambígua, links quebrados, dependência oculta ou regra de negócio sem destino.

### Implementation for User Story 3

- [x] T024 [P] [US3] Documentar `skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py` em `skills/lakeflow-pipelines/scripts/README.md` com seção `### scripts/validate_pipeline_syntax.py`, `Usage:` e `Dependencies: None`, explicando que não substitui validação/deploy Databricks
- [x] T025 [P] [US3] Criar `tests/test_validate_pipeline_syntax.py` com casos de SQL/Python sem achados, achado ERROR, aviso, arquivo inexistente e caminho de diretório inválido, verificando o código de saída documentado
- [x] T026 [US3] Executar `python3 scripts/validate_skills.py --skills-dir skills` e `python3 -m unittest discover -s tests -v`; corrigir achados estruturais e registrar comandos e resultados em `specs/001-legacy-skills-refactor/quickstart.md`
- [x] T027 [US3] Revisar ativação, não ativação, responsabilidade única, segurança, redundância e dependências em `skills/databricks-sql-quality/SKILL.md`, `skills/lakeflow-pipelines/SKILL.md` e `skills/pyspark-to-lakeflow/SKILL.md`; para cada afirmação Databricks dependente de versão, registrar URL oficial, versão consultada e status em `specs/001-legacy-skills-refactor/legacy-content-map.md`, ou marcá-la como não validada se não houver ambiente/versão-alvo; obter aprovação antes de remover ou alterar regra de negócio

**Checkpoint**: As verificações automatizadas passam e a revisão semântica documenta limitações sem afirmar que o validador substitui confirmação em ambiente real.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Confirmar cobertura integral e executar os cenários de validação antes da entrega.

- [ ] T028 Revisar todas as linhas de `specs/001-legacy-skills-refactor/legacy-content-map.md` contra `legado/` e os destinos, confirmar aprovação registrada de exclusões/alterações e executar os nove cenários de roteamento e demais verificações em `specs/001-legacy-skills-refactor/quickstart.md`; registrar a conclusão com zero fontes ou regras úteis sem destino

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sem dependências; cria as pastas de destino.
- **Foundational (Phase 2)**: depende do Setup e bloqueia as histórias; compara fontes e confirma a rastreabilidade.
- **User Story 1 (Phase 3)**: depende da fase Foundational; publica entradas autônomas e torna o catálogo descobrível.
- **User Story 2 (Phase 4)**: depende da fase Foundational e da criação das entradas da US1 para integrar as referências; os arquivos de referência e o script são unidades independentes entre si.
- **User Story 3 (Phase 5)**: depende da US2 para documentar/testar a ferramenta e da US1 para revisar os entrypoints.
- **Polish (Phase 6)**: depende das três histórias e executa a conferência final ponta a ponta.

### User Story Dependencies

- **US1 (P1)**: após Foundational; independente das outras histórias e entrega descoberta inicial.
- **US2 (P1)**: após US1 para ligar os detalhes às skills; suas referências podem ser redigidas em paralelo em arquivos diferentes.
- **US3 (P2)**: após US1 e US2; valida catálogo, ferramenta e fronteiras resultantes.

### Parallel Opportunities

- T003, T004 e T005 podem ser executadas em paralelo, pois criam `SKILL.md` distintos.
- T007–T021 podem ser executadas em paralelo depois da confirmação do inventário, pois cada tarefa cria um arquivo de referência distinto.
- T023 pode ser executada em paralelo com T007–T021 porque altera apenas o script da skill Lakeflow.
- T024 e T025 podem ser executadas em paralelo após T023; alteram arquivos distintos.
- Não paralelizar T022 com as referências: ele deve criar links somente depois que todos os destinos existirem.

## Parallel Example: User Story 2

```text
Task: T007 -> skills/databricks-sql-quality/references/table-naming.md
Task: T012 -> skills/lakeflow-pipelines/references/streaming-tables.md
Task: T019 -> skills/pyspark-to-lakeflow/references/conversion-patterns.md
Task: T023 -> skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py
```

## Implementation Strategy

### MVP First (User Story 1)

1. Concluir T001–T002 para preparar diretórios e confirmar as fontes.
2. Concluir T003–T006 para publicar os entrypoints portáteis e permitir encontrar a skill certa.
3. Validar nomes, descrições, fronteiras e descoberta inicial antes de avançar.

### Incremental Delivery

1. Entregar US1 como catálogo inicial navegável.
2. Acrescentar US2 com as referências de negócio e a ferramenta de pipeline preservada.
3. Acrescentar US3 com documentação, testes e validação estrutural/semântica.
4. Finalizar com T028 e comprovar rastreabilidade completa antes da entrega.

### Notes

- Cada linha de tarefa segue `- [ ] T### [P?] [US#?] ação e caminho(s) exato(s)`; tarefas fora das fases de história não recebem etiqueta US.
- `[P]` indica arquivos distintos sem dependência em tarefa incompleta.
- As fontes de `legado/` são somente leitura durante esta implementação; decisões de consolidação ficam nas novas skills e no mapa de conteúdo.
- Skills portáteis não dependem de `openai.yaml`, de linter DBSQL ausente ou de skills externas não incluídas no catálogo.