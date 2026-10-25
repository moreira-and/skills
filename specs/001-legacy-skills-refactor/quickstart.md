# Quickstart de Validação

Este guia valida a implementação das skills e o script local sem exigir workspace Databricks. As verificações da plataforma real permanecem externas e dependem do ambiente/versão do usuário.

## Pré-requisitos

- Python 3.11 ou superior.
- Execução a partir da raiz do repositório.
- Os arquivos em `legado/` permanecem presentes para conferir a rastreabilidade.

## Validar o catálogo

```bash
python3 scripts/validate_skills.py --skills-dir skills
```

**Esperado**: validação sem erros; nomes/diretórios correspondentes, metadados aceitos, descrições conforme a política local, links relativos existentes e documentação de todo script. O validador verifica estrutura, não semântica.

## Executar os testes

```bash
python3 -m unittest discover -s tests -v
```

**Esperado**: testes atuais do validador do catálogo e testes novos do validador de pipelines passam. Os casos do script de pipeline incluem arquivo SQL/Python válido, achado ERROR, aviso, caminho inexistente e diretório inválido; as expectativas devem testar somente comportamento documentado da ferramenta heurística.

### Resultados desta implementação

- `python3 scripts/validate_skills.py --skills-dir skills`: `Validated 3 skill(s).`
- `python3 -m unittest discover -s tests -v`: 18 testes passaram.
- `python3 -m unittest discover -s tests -p 'test_validate_pipeline_syntax.py' -v`: 7 testes passaram.
- Compatibilidade real de sintaxe/deploy Databricks: não validada; não foi informado workspace ou versão-alvo.

## Revisão de cobertura e independência

1. Conferir cada linha de [legacy-content-map.md](legacy-content-map.md) contra o arquivo-fonte e a skill/reference/script de destino.
2. Para cada regra útil, confirmar uma localização canônica, sem conflito não documentado; rever especialmente a regra de prefixos e a equivalência entre dedupe imperativo e CDC.
3. Não remover nem alterar semanticamente regra que afete negócio, qualidade, segurança, operação ou salvaguardas sem justificativa e aprovação registrada da pessoa solicitante ou responsável de negócio designada.
4. Usar a suíte fixa abaixo com duas pessoas revisoras, sem consulta entre elas; ambas devem escolher a mesma skill primária para cada solicitação.
5. Confirmar que ferramentas e referências ausentes no legado não são anunciadas como disponíveis.
6. Para cada afirmação Databricks dependente de versão, registrar URL oficial, versão consultada e status no mapa de conteúdo; sem versão/ambiente-alvo, preservar ressalva e marcar como não validada.

| Capacidade esperada | Solicitação de teste |
|---|---|
| `databricks-sql-quality` | Revisar se nomes de tabelas e colunas seguem as convenções locais. |
| `databricks-sql-quality` | Reestruturar um SQL para melhorar legibilidade, aliases e organização em CTEs. |
| `databricks-sql-quality` | Declarar tipos e comentários de negócio para colunas publicadas. |
| `lakeflow-pipelines` | Criar ingestão incremental de uma fonte append-only. |
| `lakeflow-pipelines` | Decidir entre streaming table e materialized view para uma transformação. |
| `lakeflow-pipelines` | Configurar expectativas de qualidade ou CDC em um pipeline existente. |
| `pyspark-to-lakeflow` | Migrar um conjunto de scripts PySpark para SQL declarativo com DABs. |
| `pyspark-to-lakeflow` | Inventariar dependências, propor nomes canônicos e obter aprovação antes de gerar artefatos. |
| `pyspark-to-lakeflow` | Validar artefatos migrados e preparar o manifesto de entrega. |

**Esperado**: as duas pessoas revisoras concordam nos nove casos; 100% das fontes e regras úteis têm destino rastreável; cada exclusão/alteração tem aprovação; nenhuma skill tem fronteira ambígua; nenhum link local quebrado ou dependência oculta.

## Limite da validação

Os comandos locais não verificam se um pipeline pode ser publicado em um workspace Databricks. O script de sintaxe usa heurísticas; `databricks bundle validate` e execução real só são aplicáveis com CLI, configuração e ambiente correspondentes. Não afirmar que deploy foi validado quando esses pré-requisitos não estiverem disponíveis.