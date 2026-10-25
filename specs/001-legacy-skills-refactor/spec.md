# Feature Specification: Refatoração das Skills Legadas

**Feature Branch**: `[main]`

**Created**: 2026-10-25

**Status**: Draft

**Input**: User description: "Em `legado/` há arquivos legados sobre skills locais. Quero refatorá-los aplicando as melhores práticas de mercado: interpretar o conteúdo, organizá-lo em skills independentes com responsabilidades claras, aplicar as práticas definidas na fundação deste repositório e otimizar as skills sem remover seu valor de negócio."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Encontrar a orientação correta (Priority: P1)

Uma pessoa que cria ou mantém pipelines precisa identificar rapidamente qual skill consultar para uma tarefa, sem carregar instruções que pertencem a outra responsabilidade.

**Why this priority**: A descoberta clara e a independência das skills são o principal resultado solicitado e reduzem orientações irrelevantes ou conflitantes.

**Independent Test**: Revisores recebem solicitações representativas dos temas legados e conseguem selecionar a skill responsável usando sua descrição e escopo, sem depender de carregar outra skill para compreender a orientação principal.

**Acceptance Scenarios**:

1. **Given** uma solicitação relacionada a um tema coberto pelo legado, **When** a pessoa consulta as descrições e limites das skills, **Then** identifica uma capacidade principal responsável e sabe quando não usar cada skill.
2. **Given** duas skills com assuntos complementares, **When** uma tarefa exige ambas, **Then** cada skill contribui apenas com sua responsabilidade e as referências entre elas indicam claramente quando consultar a outra.

### User Story 2 - Migrar sem perder valor de negócio (Priority: P1)

Uma pessoa responsável por migrar ou manter pipelines precisa continuar aplicando as decisões, salvaguardas e validações de negócio presentes nos materiais legados.

**Why this priority**: Uma reorganização estrutural só é útil se preservar regras que protegem a semântica, a qualidade e a operação dos pipelines.

**Independent Test**: Compare o inventário dos materiais de origem com as skills resultantes e confirme que toda regra útil está preservada ou tem uma decisão de exclusão/alteração documentada e aprovada pela pessoa solicitante ou responsável de negócio designada.

**Acceptance Scenarios**:

1. **Given** os arquivos legados e seus exemplos, **When** a migração é revisada, **Then** regras de conversão, arquitetura, qualidade, nomenclatura, tipagem, documentação, implantação e validação permanecem acessíveis na responsabilidade adequada.
2. **Given** instruções duplicadas, sobrepostas ou candidatas a exclusão/alteração, **When** são consolidadas ou modificadas, **Then** diferenças semânticas ficam registradas e nenhuma regra útil é removida ou alterada sem aprovação da pessoa solicitante ou responsável de negócio designada.

### User Story 3 - Revisar e evoluir o catálogo (Priority: P2)

Uma pessoa mantenedora do catálogo precisa avaliar se as skills seguem a fundação do repositório e podem evoluir sem criar dependências ocultas ou itens difíceis de manter.

**Why this priority**: A aderência às convenções e a revisabilidade evitam que a refatoração introduza dívida no catálogo.

**Independent Test**: Validar a estrutura e os metadados de todas as skills resultantes e realizar revisão semântica de responsabilidade única, ativação, referências, segurança e utilidade dos scripts.

**Acceptance Scenarios**:

1. **Given** as skills refatoradas, **When** são avaliadas segundo a fundação do repositório, **Then** seguem o contrato do catálogo e não dependem de metadados ou comportamento específico de um consumidor sem declarar essa limitação.
2. **Given** ferramentas executáveis preservadas, **When** uma pessoa revisa cada ferramenta, **Then** encontra instruções de uso, dependências, tratamento de erros e limites do que a ferramenta valida.

### Edge Cases

- Um arquivo de origem é duplicado ou tem nome semelhante a outro: seu conteúdo é comparado e contabilizado, sem duplicar a regra nem ignorar diferenças.
- Uma regra aparece em mais de um domínio ou conflita com outra: a regra canônica e suas referências ficam claras; conflito não resolvido é registrado para decisão, em vez de ser escondido.
- Uma orientação depende de documentação ou de versão externa que pode ter mudado: a dependência e a necessidade de confirmação são explicitadas, sem afirmar compatibilidade não verificada.
- Um script legado não tem uma skill de destino óbvia ou sua utilidade não está comprovada: a decisão de manter, adaptar ou retirar deve ser justificada e não criar uma skill apenas para acomodá-lo.
- Uma referência local ou ferramenta citada não existe no catálogo atual: a skill não deve apresentar o recurso ausente como dependência disponível sem registrar a limitação.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A refatoração MUST inventariar todos os arquivos fornecidos em `legado/`, incluindo documentos, arquivos de metadados e ferramentas executáveis, e registrar para cada fonte seu destino ou justificativa de não incorporação.
- **FR-002**: Cada skill resultante MUST ter uma responsabilidade principal identificável, descrição de ativação precisa, limites de uso e instruções essenciais suficientes para entregar sua capacidade sem exigir o carregamento de outra skill.
- **FR-003**: Referências entre skills MUST ser explícitas, relativas e limitadas a complementaridades necessárias; elas não podem transformar uma skill em pré-requisito implícito para compreender a responsabilidade principal de outra.
- **FR-004**: A migração MUST preservar e atribuir às responsabilidades apropriadas as regras, decisões, exemplos, gates, alertas operacionais e critérios de validação que sustentam o valor de negócio do material legado.
- **FR-005**: Conteúdo duplicado MUST ser consolidado sem perda semântica; diferenças, contradições e regras removidas ou alteradas MUST ter tratamento rastreável, justificativa e aprovação da pessoa solicitante ou responsável de negócio designada antes da remoção ou mudança semântica.
- **FR-006**: As skills MUST seguir o contrato e as práticas da fundação do repositório, incluindo metadados permitidos, limites de nome e descrição, orientações concisas e referências locais válidas.
- **FR-007**: Qualquer ferramenta executável mantida MUST ter propósito claro, comportamento determinístico quando viável, erros compreensíveis, instruções de uso e dependências documentadas; seu escopo e limitações MUST permanecer explícitos.
- **FR-008**: Regras dependentes de versões, produtos ou consumidores específicos MUST explicitar a dependência e não presumir compatibilidade universal ou vigência sem confirmação adequada.
- **FR-009**: A conclusão MUST incluir validação estrutural e revisão semântica de responsabilidade única, limites de ativação, correção, segurança, contradições, redundância, referências e utilidade das ferramentas.
- **FR-010**: A refatoração MUST evitar skills ou artefatos de preenchimento; cada nova capacidade publicada precisa corresponder a uma necessidade sustentada pelo inventário e pela revisão.
- **FR-011**: O resultado MUST permitir rastrear o conteúdo de origem relevante até a skill ou referência que o preserva, mantendo registro das decisões de consolidação e descarte.
- **FR-012**: Uma regra MUST ser considerada útil quando sua remoção ou alteração puder afetar semântica de negócio, qualidade, segurança, operação ou uma salvaguarda de migração; exclusões e mudanças semânticas devem permanecer pendentes até aprovação da pessoa solicitante ou responsável de negócio designada.

### Key Entities *(include if feature involves data)*

- **Fonte legada**: Documento, configuração ou ferramenta em `legado/`; tem conteúdo, possíveis duplicatas e uma decisão de destino.
- **Skill**: Capacidade publicada no catálogo; tem responsabilidade, público/ativação, limites, instruções essenciais e referências opcionais.
- **Regra de negócio**: Decisão, salvaguarda, exemplo ou validação que precisa continuar orientando o uso dos pipelines.
- **Referência**: Conteúdo de apoio ligado explicitamente a uma skill e consultado quando necessário para uma tarefa específica.
- **Ferramenta executável**: Script de validação ou apoio que pode ser preservado, ajustado ou removido mediante justificativa e documentação.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos arquivos legados fornecidos têm uma destinação ou justificativa registrada e verificável.
- **SC-002**: 100% das regras classificadas como úteis têm localização canônica; toda regra excluída ou alterada tem justificativa e aprovação registrada da pessoa solicitante ou responsável de negócio designada antes da mudança.
- **SC-003**: Em uma suíte fixa de nove solicitações (três por capacidade), duas pessoas revisoras mapeiam independentemente 100% dos casos para a mesma skill primária, sem casos ambíguos.
- **SC-004**: Todas as skills resultantes passam pelas verificações estruturais aplicáveis ao catálogo e não contêm referências locais quebradas.
- **SC-005**: A revisão semântica não encontra dependências obrigatórias ocultas, responsabilidades duplicadas sem justificativa, contradições não registradas ou ferramentas sem instruções de uso e dependências.
- **SC-006**: A comparação entre origem e resultado encontra zero omissões de salvaguardas para identificar mudanças semânticas, bloqueios operacionais e pendências antes de concluir uma migração.

## Assumptions

- A constituição e o contrato documentados na fundação deste repositório prevalecem sobre convenções incompatíveis presentes nos arquivos legados.
- A quantidade final de skills será determinada por responsabilidades distintas e capacidades reutilizáveis, não pelo número de arquivos de origem.
- O conteúdo técnico específico de Databricks permanece útil ao público pretendido, mas orientações sujeitas a mudanças externas precisam ser tratadas como dependentes de versão e verificadas conforme necessário.
- A especificação não altera a constituição, as ferramentas gerais do catálogo ou outros conteúdos fora do escopo da refatoração do material legado.
- A disposição final dos originais, de eventuais metadados específicos de consumidores e de cada ferramenta será decidida durante o planejamento, com rastreabilidade e sem descarte silencioso.