# Scripts da Skill Lakeflow

### scripts/validate_pipeline_syntax.py

Validador estático baseado em expressões regulares para padrões comuns em definições SQL/Python de Lakeflow Declarative Pipelines. Não é parser SQL, não certifica compatibilidade de versão e não substitui validação de bundle ou execução em workspace Databricks.

Usage:
Dependencies: None.

```bash
python3 skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py caminho/arquivo.sql
python3 skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py caminho/arquivo.py
python3 skills/lakeflow-pipelines/scripts/validate_pipeline_syntax.py --dir caminho/do/pipeline
```

Retorna `0` sem erros, inclusive quando há somente avisos heurísticos; retorna `1` para achados `ERROR` ou entradas inválidas. Uso sem arquivos ou `--dir` inválido retorna erro de argumentos.

**Dependencies:** None.