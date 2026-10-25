---
name: lakeflow-pipelines
description: Orienta a autoria e revisão de pipelines declarativos Databricks em SQL ou Python. Use when escolher objetos, modelar ingestão, CDC, qualidade, camadas ou operação de Lakeflow.
---

# Lakeflow Declarative Pipelines

## Responsabilidade

Orientar decisões e revisões próprias de Lakeflow Declarative Pipelines: tipo de objeto, incrementalidade, CDC, expectativas, organização do grafo e operação. Convenções de nomenclatura e estilo fornecidas pela empresa podem complementar o trabalho, mas não são pré-requisitos para usar esta skill.

## Quando não usar

- Não use para aplicar convenções gerais de SQL a consultas fora do contexto de pipeline.
- Não use como processo completo de conversão de um conjunto de jobs PySpark para SQL/DAB.
- Não afirme compatibilidade de sintaxe, APIs Python ou configuração de bundle sem confirmar a versão/documentação aplicável.

## Fluxo

1. Identifique fontes, destino, incrementalidade, chaves, sequência, expectativa de latência e ambiente.
2. Nomeie identificadores de catálogo, schema, tabela e coluna no singular; não altere nomes exigidos pela gramática ou API da plataforma.
3. Escolha o tipo de objeto de acordo com o ciclo dos dados e o comportamento necessário; explique riscos de recomputação, append-only e mudanças semânticas.
4. Para CDC ou deduplicação, confirme chave e ordenação confiável; não converta padrões imperativos em operações declarativas sem verificar equivalência.
5. Defina explicitamente o efeito de cada regra de qualidade sobre linhas e atualização do pipeline.
6. Confirme sintaxe e APIs dependentes de versão em fonte oficial; se a versão-alvo não estiver disponível, mantenha a ressalva e marque a compatibilidade como não validada.
7. Trate validações estáticas como heurísticas e separe seus achados da validação real de bundle ou execução no workspace.

## Referências

- [Streaming tables](references/streaming-tables.md)
- [Materialized views](references/materialized-views.md)
- [CDC, dedupe e SCD](references/apply-changes-cdc.md)
- [Expectations de qualidade](references/data-quality-expectations.md)
- [Arquitetura medallion](references/medallion-architecture.md)
- [Escolha entre SQL e Python](references/python-vs-sql.md)
- [Implantação, execução e monitoramento](references/deployment-execution.md)
- [Validador estático de sintaxe](scripts/README.md)