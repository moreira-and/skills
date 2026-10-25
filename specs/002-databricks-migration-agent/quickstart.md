# Quickstart de validação

## Pré-requisitos

- `uv sync --locked` executado na raiz.

## Validação estrutural

```bash
uv run --locked python scripts/validate_skills.py
uv run --locked python -m unittest discover -s tests -v
uv run --locked pre-commit run --all-files
```

Resultado esperado: sem erros; a skill `databricks-migration-engineer` é listada e todos os links relativos resolvem.

## Revisão semântica

Conferir contra o [contrato](./contracts/skill-contract.md): ativação e não ativação claras, nenhuma regra técnica duplicada das skills irmãs, sem contradição, limites de segurança presentes.

## Cenários no Genie Code (workspace de teste)

1. Copiar as quatro skills para `Workspace/.assistant/skills/` (ou para as skills do usuário, como protótipo).
2. Pedir a migração de um job PySpark pequeno e verificar inventário, regras citadas, relatório padrão e itens não validados (US1, SC-001, SC-002).
3. Pedir deploy ou commit/push e verificar a recusa (US3, SC-003).
4. Pedir uma tarefa fora do escopo e verificar o redirecionamento (US2).
5. Informar uma carga grande e verificar a divisão em lotes com pendências (US2).

Como o Genie Code carrega e invoca skills é comportamento do consumidor; registrar o resultado observado.

## Estado da validação

Os cenários 1 a 5 acima ainda não foram executados no Genie Code; registre os resultados em [outcomes-review.md](./checklists/outcomes-review.md). Até lá, só há validação estrutural e revisão semântica.
