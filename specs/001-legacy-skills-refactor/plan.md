# Implementation Plan: Refatoração das Skills Legadas

**Branch**: `main` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-legacy-skills-refactor/spec.md`

## Summary

Converter o inventário de `legado/` em capacidades reutilizáveis no catálogo portátil `skills/`, com fronteiras claras, referências focadas e rastreabilidade das fontes. A divisão inicial proposta tem três skills: qualidade e convenções DBSQL; autoria e operação de Lakeflow Declarative Pipelines; migração PySpark para Lakeflow SQL/DAB. O conteúdo será preservado como política local quando for regra organizacional, não apresentado como padrão universal. O validador de pipeline permanece uma ferramenta heurística documentada e testada; não será prometido um linter DBSQL ausente do repositório.

## Technical Context

**Language/Version**: Markdown e YAML interoperáveis; Python 3.11 ou superior para ferramentas e testes locais.

**Primary Dependencies**: Nenhuma dependência de runtime nova. O validador do catálogo e os testes atuais usam a biblioteca padrão Python; ferramentas de Databricks são dependências externas opcionais do trabalho real do usuário.

**Storage**: Arquivos no repositório; nenhuma persistência de runtime.

**Testing**: `python3 scripts/validate_skills.py --skills-dir skills`; `python3 -m unittest discover -s tests -v`; casos unitários para o validador heurístico; revisão semântica manual conforme a constituição.

**Target Platform**: Catálogo de Agent Skills em `skills/`, portável entre consumidores compatíveis; comportamento de descoberta/invocação específico de cada agente não é presumido.

**Project Type**: Documentação de skills e utilitários locais de validação.

**Performance Goals**: N/A; validação local de um catálogo pequeno, sem requisito de latência ou vazão.

**Constraints**: Seguir o contrato em `README.md`; responsabilidade principal única; nomes e descrições aceitos pelo validador; referências locais relativas e até um diretório de profundidade; scripts documentados em `scripts/README.md`; não depender de conteúdo inexistente; para afirmações de produto dependentes de versão, registrar fonte oficial, versão consultada e status da checagem; sem evidência ou versão-alvo, manter a ressalva e marcar como não validado; manter `legado/` intacto como fonte fornecida.

**Scale/Scope**: 22 arquivos de origem entre três documentos-raiz, referências de domínio, dois YAMLs de consumidor, uma duplicata exata e um script de validação. Escopo inicial de três capacidades, sujeito à validação de independência dos casos de uso; nenhum catálogo ou skill placeholder.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Interoperability First — PASS**: publicar no contrato portátil de `skills/`; não converter `openai.yaml` para frontmatter ou invocação não padronizados. Documentar limitações de descoberta específica por agente.
- **II. One Clear Responsibility — PASS**: separar as três capacidades candidatas e manter detalhes em referências explícitas; nenhuma skill depende de outra para explicar sua capacidade essencial.
- **III. Safe, Reviewable Execution — PASS WITH CONDITIONS**: reter o validador de pipeline apenas com limites heurísticos explícitos, tratamento de erro testado, acesso local mínimo e instruções de uso/dependências. Novas ferramentas só se necessárias.
- **IV. Validation Is Necessary, Not Sufficient — PASS**: executar validador do catálogo e testes; complementar com revisão semântica e inspeção de links/limites de ativação.
- **V. Traceable, Incremental Evolution — PASS**: mapa de fontes e decisões será mantido com os artefatos da feature. Não alterar nem apagar `legado/` nesta migração; preservar a origem por ser conteúdo fornecido pelo usuário.

Não há violações constitucionais que exijam exceção. A dependência de versões Databricks será registrada e validada para cada instrução sujeita a mudança antes da publicação.

**Re-check após Phase 1 design — PASS**: o catálogo escolhido mantém formato portátil; as três capacidades têm fronteiras independentes com referências opcionais; o script heurístico tem escopo e testes propostos; o quickstart combina validação estrutural e revisão semântica; o mapa preserva proveniência e aprovação de mudanças sem alterar as fontes; e afirmações de produto têm critério de evidência/versionamento ou status não validado. O linter DBSQL ausente e documentação sem evidência são explicitamente excluídos de qualquer promessa de disponibilidade/compatibilidade.

## Project Structure

### Documentation (this feature)

```text
specs/001-legacy-skills-refactor/
├── plan.md
├── research.md
├── data-model.md
├── legacy-content-map.md
├── quickstart.md
└── tasks.md                 # Gerado depois por /speckit-tasks
```

Não serão criados contratos de API: o resultado é um catálogo de instruções sem interface de serviço externa.

### Source Code (repository root)

```text
skills/
├── databricks-sql-quality/
│   ├── SKILL.md
│   └── references/          # Regras locais de nomes, tipos, comentários e legibilidade
├── lakeflow-pipelines/
│   ├── SKILL.md
│   ├── references/          # Objetos, CDC, qualidade, medallion, linguagem e operação
│   └── scripts/
│       ├── README.md
│       └── validate_pipeline_syntax.py
└── pyspark-to-lakeflow/
    ├── SKILL.md
    └── references/          # Conversões, DABs e checklist/manifesto

scripts/validate_skills.py  # Validador estrutural do catálogo, sem mudança prevista
tests/
├── test_validate_skills.py
└── test_validate_pipeline_syntax.py  # Testes a adicionar para a ferramenta migrada

legado/                      # Fontes de entrada preservadas, sem edição ou remoção
```

**Structure Decision**: usar o catálogo portátil `skills/` com uma pasta por capacidade. Não publicar cópias específicas em `.github/skills/` nem manter metadata específica de consumidor como requisito; eventual adaptação para consumidor é escopo posterior e só com compatibilidade verificada. `legacy-content-map.md` preserva rastreabilidade das fontes e orienta a migração sem incorporar registros de origem no runtime das skills.

## Complexity Tracking

Não há violações constitucionais ou componentes adicionais que exijam justificativa.
