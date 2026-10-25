# Pesquisa: Refatoração das Skills Legadas

## Decisão 1: Publicar no catálogo portátil

**Decision**: Criar as capacidades em `skills/<nome>/SKILL.md`, usando apenas campos suportados pelo contrato local. Não publicar cópias automáticas em `.github/skills/`.

**Rationale**: A fundação define `skills/` como catálogo portátil e informa que `.github/skills/` contém comandos Copilot, não skills corporativas. Os YAMLs legados usam `interface`, imagens e invocação `$skill`, sem garantir portabilidade.

**Alternatives considered**: Manter apenas os arquivos `openai.yaml` do legado; rejeitado por depender de formato e comportamento de consumidor. Duplicar já para Copilot; rejeitado por ampliar o escopo antes de verificar descoberta, permissões e suporte.

## Decisão 2: Iniciar com três responsabilidades

**Decision**: Planejar três capacidades independentes: qualidade/convenções DBSQL; autoria/operação de Lakeflow Declarative Pipelines; migração PySpark→Lakeflow SQL/DAB.

**Rationale**: Cada núcleo tem usuário, ativação e fluxo próprios. A migração coordena inventário, gates, equivalência e entrega; não deve absorver as regras gerais de qualidade SQL nem o modelo de autoria de pipeline. A skill de pipeline pode ser usada sem o processo de migração.

**Alternatives considered**: Uma skill monolítica; rejeitada por contrariar responsabilidade única e carregar detalhes irrelevantes. Uma skill por arquivo-fonte; rejeitada por replicar a fragmentação legada e criar unidades sem capacidade autônoma. O número permanece sujeito à revisão de casos de ativação antes da publicação.

## Decisão 3: Tratar regras locais como política, não padrão de mercado

**Decision**: Preservar nomenclatura, tipagem, comentários e estilo como convenções organizacionais identificadas como tais; documentar exceções e resolver divergências usando uma fonte canônica.

**Rationale**: O legado agrega valor de governança, mas limites como prefixos, aliases, `SELECT *` e tamanho mínimo de `COMMENT` não são universais. O objetivo é aplicar a fundação do repositório e manter a política local sem apresentá-la como requisito universal da plataforma.

**Alternatives considered**: Converter todas as regras locais em afirmações de mercado; rejeitado por imprecisão. Remover tais regras por não serem universais; rejeitado por perder valor de negócio.

## Decisão 4: Consolidar a duplicata e resolver conflitos com rastreabilidade

**Decision**: Consolidar `python-vs-sql.md` e `python-vs-sql (1).md` em uma referência; tratar `column-naming.md` como fonte canônica para prefixos, corrigindo a menção conflitante a `nm_` na referência duplicada. Registrar fontes e decisões em `legacy-content-map.md`.

**Rationale**: Os arquivos Python-vs-SQL são idênticos. A regra de colunas de uma fonte proíbe `nm_`; referências desatualizadas não podem reintroduzir o prefixo. O mapa mantém destino, consolidação e justificativa para cada arquivo.

**Alternatives considered**: Preservar ambas as cópias; rejeitado por redundância. Excluir os originais; rejeitado porque são entradas fornecidas e a rastreabilidade deve permanecer; a migração não altera `legado/`.

## Decisão 5: Não prometer ferramentas inexistentes

**Decision**: Não documentar como executável o `dbsql_linter.py`, auto-fix ou documentação/referências locais que não estão no inventário. Preservar `validate_pipeline_syntax.py` somente como triagem heurística, com revisão de erros e testes unitários.

**Rationale**: O catálogo não contém o linter DBSQL prometido pelo `SKILL.md` legado, nem referências como `naming-governance.md` e `audit-columns.md`. O utilitário de pipeline usa expressões regulares e não substitui validação real; a documentação deve declarar esse limite.

**Alternatives considered**: Criar um linter DBSQL substituto; rejeitado por ampliar escopo e potencialmente mudar regras sem solicitação. Tratar o validador heurístico como parser ou gate de deploy; rejeitado por falsos positivos/negativos.

## Decisão 6: Preservar exemplos de plataforma como condicionais/versionados

**Decision**: Manter o valor de CDC, expectations, streaming tables, materialized views, SQL/Python e DABs, mas indicar dependência da versão e do ambiente quando a sintaxe ou configuração puder mudar. Confirmar documentação oficial vigente antes de publicar afirmações operacionais específicas.

**Rationale**: Os artefatos de origem não registram uma matriz de versões Databricks; portanto, não é seguro transformar exemplos em configuração universal. Regras de negócio e critérios de decisão permanecem, enquanto sintaxe configurável é explicitamente exemplo.

**Alternatives considered**: Fixar versão presumida com base apenas no conteúdo legado; rejeitado por falta de evidência. Remover todo conteúdo dependente de produto; rejeitado por eliminar o propósito comercial do material.

## Decisão 7: Validar localmente sem impor dependência nova

**Decision**: Usar o validador do catálogo e testes unitários da biblioteca padrão. Testar o validador de pipeline com casos representativos de sucesso, erro, avisos e entradas inválidas.

**Rationale**: `scripts/validate_skills.py` e os testes atuais não exigem bibliotecas externas. A ferramenta de pipeline pode permanecer autocontida e testável. Revisão humana continua obrigatória para semântica, segurança, clareza e compatibilidade.

**Alternatives considered**: Acrescentar parser SQL de terceiros; rejeitado para esta migração sem requisitos para AST ou análise completa. Executar apenas validador estrutural; rejeitado porque não comprova qualidade semântica.

## Lacunas resolvidas

Não há decisão de produto bloqueante pendente para o desenho. A pesquisa local não certifica a versão atual de APIs Databricks. Durante a implementação, afirmações operacionais deverão ser verificadas em documentação oficial para a versão-alvo; se o ambiente-alvo não estiver disponível, os textos devem manter a ressalva e não alegar validação.