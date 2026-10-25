# Feature Specification: Databricks Migration Specialist Agent

**Feature Branch**: `002-databricks-migration-agent`

**Created**: 2026-10-25

**Status**: Draft

**Input**: User description: "crie um agente especialista em migração para o databricks. ele deve ter mindset de engenheiro de dados e utilizar as regras locais criadas. crie este agente com as melhores práticas de mercado seguindo a estrutura recomendada. Ele vai servir de instrução em massa para trabalho no databricks."

## Clarifications

### Session 2026-10-25

- Q: Qual nível de autonomia o agente deve ter no Databricks? → A: Será usado no Genie Code embarcado no Databricks, com acesso ao workspace de teste; não faz deploy, commits nem push.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Delegate a migration to a specialist agent (Priority: P1)

A data engineer asks the agent to migrate a legacy workload (for example, imperative PySpark jobs) to Databricks. The agent behaves like a senior data engineer: it first inventories sources, destinations, keys, schedules, volumes and consumers, then applies the catalog's local rules (the existing Databricks SQL quality, Lakeflow pipelines and PySpark-to-Lakeflow skills) to plan and execute the conversion while preserving behavior.

**Why this priority**: This is the core value: a single, reusable specialist that applies the organization's rules consistently instead of each engineer re-explaining them.

**Independent Test**: Give the agent a small legacy job and verify it produces an inventory, a migration plan citing the applicable local rules, converted artifacts, and a list of unvalidated assumptions.

**Acceptance Scenarios**:

1. **Given** a legacy job and the local skills catalog, **When** the engineer requests a migration, **Then** the agent inventories the job before proposing changes and cites which local rules it applies at each step.
2. **Given** a request where a local rule conflicts with general market practice, **When** the agent decides, **Then** it follows the local rule and records the divergence.
3. **Given** a platform behavior or syntax that cannot be confirmed for the target version, **When** the agent reports results, **Then** it marks it as not validated instead of asserting compatibility.

---

### User Story 2 - Use the agent as mass instruction for many Databricks tasks (Priority: P1)

A team lead uses the agent as a standing instruction set so that many engineers and many tasks (batches of jobs, tables, pipelines) follow the same method, output format and quality bar.

**Why this priority**: The user states the agent's purpose is mass instruction; consistency at scale is the main outcome.

**Independent Test**: Run the agent on three different workloads and verify each produces the same structure of deliverables (inventory, plan, conversion, validation notes) and the same rule citations.

**Acceptance Scenarios**:

1. **Given** several workloads of different complexity, **When** each is processed, **Then** every result follows the same defined workflow and report structure.
2. **Given** a very large workload, **When** the agent proceeds, **Then** it splits work into reviewable batches and states what remains.
3. **Given** a task unrelated to Databricks migration or data engineering, **When** requested, **Then** the agent declines or redirects instead of improvising.

---

### User Story 3 - Safe, reviewable behavior (Priority: P2)

A reviewer needs confidence that the agent acts within clear limits: it does not run destructive actions, expose secrets or data, or claim validation it did not perform.

**Why this priority**: Migrations touch production data; trust depends on explicit boundaries.

**Independent Test**: Ask the agent to perform a destructive or secret-exposing action and verify it refuses or asks for confirmation; verify reports separate static checks from real execution.

**Acceptance Scenarios**:

1. **Given** a request that would delete data, overwrite production objects or reveal credentials, **When** the agent evaluates it, **Then** it requires explicit confirmation or declines.
2. **Given** a completed migration, **When** the agent reports, **Then** it distinguishes static review from real workspace validation and lists residual risks.

---

### User Story 4 - Maintainable and discoverable agent definition (Priority: P3)

A catalog maintainer can find, validate and evolve the agent definition, which is a skill in the Agent Skills format.

**Why this priority**: Long-term maintainability; the agent must not drift from the local rules it relies on.

**Independent Test**: A maintainer reads the catalog documentation, locates the agent, and runs the catalog's validation without errors.

**Acceptance Scenarios**:

1. **Given** the catalog, **When** a maintainer looks for the agent, **Then** it is documented with its purpose, limits, and relationship to the local skills.
2. **Given** a local rule is updated, **When** the agent is reviewed, **Then** it references the rule rather than duplicating it, so no contradiction arises.

---

### Edge Cases

- The legacy workload is not PySpark (for example, SQL scripts, ETL tools): the agent states which parts of the method apply and which are out of local-rule coverage.
- The target Databricks version or feature is unknown: compatibility is marked as not validated.
- Local rules are silent on a decision: the agent applies a documented market practice and flags it as an assumption.
- Local rules contradict each other: the agent surfaces the conflict and asks for a decision.
- The input lacks keys, ordering or latency expectations needed for correct CDC/deduplication: the agent asks rather than guessing.
- No workspace access is available: the agent delivers static results and clearly states real validation is pending.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The agent MUST adopt a senior data-engineer posture: understand data, keys, volumes, consumers and risks before changing anything, and prioritize correctness and behavior preservation over speed.
- **FR-002**: The agent MUST apply the existing local rules (the catalog's Databricks SQL quality, Lakeflow pipelines and PySpark-to-Lakeflow skills) by reference and MUST NOT duplicate or contradict their content.
- **FR-003**: Where local rules and general practice differ, the agent MUST follow local rules and record the divergence.
- **FR-004**: The agent MUST follow a defined, repeatable workflow (inventory, plan, convert, validate, report) for every task.
- **FR-005**: The agent MUST produce a consistent report structure including applied rules, assumptions, unvalidated items and residual risks.
- **FR-006**: The agent MUST mark version-dependent syntax or platform behavior as not validated when it cannot be confirmed against authoritative documentation.
- **FR-007**: The agent MUST separate static/heuristic checks from real validation in a workspace, and MUST NOT claim the latter unless performed.
- **FR-008**: The agent MUST ask for missing critical information (keys, ordering, latency, ownership, environment) instead of assuming.
- **FR-009**: The agent MUST NOT deploy, commit or push, and MUST NOT act on production; it MAY read and validate only in the test workspace. It MUST require explicit confirmation before destructive or irreversible actions even there, and MUST NOT expose secrets or sensitive data.
- **FR-010**: The agent MUST support batch work by splitting large workloads into reviewable units and reporting progress and remaining items.
- **FR-011**: The agent MUST have a precise scope and activation description, and MUST decline or redirect requests outside Databricks migration and data engineering.
- **FR-012**: The agent MUST be delivered as a skill following the Agent Skills standard (the structure Genie Code consumes), with clear identity, scope, workflow, constraints, permission limits and output format, keeping the main file concise and loading detail from references on demand.
- **FR-013**: The agent MUST be documented in the catalog README (purpose, limits, relationship to local skills, consumer-specific caveats) and MUST pass the catalog's structural validation.
- **FR-014**: The agent MUST remain compatible with the catalog's interoperability principle; any consumer-specific behavior MUST be documented as a limitation rather than assumed portable.
- **FR-015**: The agent MUST be usable within Genie Code (the assistant embedded in Databricks); its definition and the catalog documentation MUST state this consumer's discovery and permission limits rather than assuming portability.

### Key Entities

- **Migration Agent (skill)**: The specialist definition with identity, scope, workflow, constraints and output format.
- **Local Rule Set**: The existing catalog skills the agent defers to.
- **Migration Task**: A unit of legacy workload with sources, destinations, keys, schedules and consumers.
- **Migration Report**: Standard deliverable listing inventory, applied rules, assumptions, unvalidated items and risks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a review of 5 sample migration requests, 100% of agent outputs follow the same workflow and report structure.
- **SC-002**: In those samples, 100% of decisions covered by a local rule cite that rule, and 0 contradict it.
- **SC-003**: 100% of out-of-scope, destructive, deploy, commit or push sample requests are declined or require explicit confirmation.
- **SC-004**: 100% of reports distinguish static review from real validation and list unvalidated items.
- **SC-005**: A maintainer can locate the agent and understand its scope and limits from the documentation in under 5 minutes.
- **SC-006**: The agent definition passes the catalog's structural validation with no errors and is judged free of contradictions in human review.

## Assumptions

- "Agent" means a skill in the Agent Skills format, since Genie Code has no separate agent format; the exact file layout is defined in the plan.
- "Local rules" means the three existing skills under `skills/`.
- The primary consumer is Genie Code embedded in Databricks, with access to the test workspace only; deployment and version-control publishing are done by humans outside the agent.
- The agent is primarily conversational/instructional; it relies on tools available in the consumer and does not add new scripts unless planning shows a need.
- Output language follows the local rules' language (Portuguese) by default, matching the engineer's request.
- Scope is migration to Databricks (Lakeflow SQL/Python, DAB) with a focus on PySpark sources; other source technologies are handled best-effort with explicit coverage limits.
- No Git branch is created for this feature; the spec directory is the source of traceability.
