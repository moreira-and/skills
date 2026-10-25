# Arquitetura Medallion e Grafo Declarativo

As camadas bronze, silver e gold são uma organização recomendada, não uma obrigação universal. Escolha limites conforme as responsabilidades e consumidores dos dados.

## Responsabilidade por camada

- **Bronze**: ingestão bruta, transformações mínimas e preservação da origem; considerar streaming table para ingestão incremental.
- **Silver**: limpeza, normalização, enriquecimento e tratamento de duplicação/CDC quando aplicável.
- **Gold**: conjuntos de consumo, métricas e agregações; materialized view pode ser adequada quando o refresh e o custo atendem ao caso.

## Grafo declarativo

- O pipeline pode ser composto por arquivos SQL/Python incluídos na configuração do recurso.
- Cada objeto deve ter uma definição declarativa própria; dependências são determinadas pelas relações de leitura/saída compatíveis com o motor.
- Não transportar controle imperativo de ordem de `INSERT`/blocos de job para dentro da definição declarativa sem confirmar o modelo vigente.
- Para várias fontes destinadas ao mesmo alvo, avaliar flows distintos. Confirmar a sintaxe e a semântica de append/merge na versão instalada.
- O legado cita `CREATE FLOW ... AS INSERT INTO ... BY NAME SELECT ...` e `APPEND FLOW` como opções para múltiplas origens; tratá-las apenas como nomes de padrões a investigar, nunca como sintaxe validada para a versão atual.

## Estrutura ilustrativa

```text
pipelines/
└── nome_do_pipeline/
    ├── explorations/       # opcional; fora do grafo publicado
    └── transformations/
        ├── 01_bronze_source.sql
        ├── 02_silver_transform.sql
        └── 03_gold_metrics.sql
```

Os nomes e a disposição de pastas são exemplos, não estrutura obrigatória. Não confunda a camada arquitetural com o nome do objeto; use os padrões de nomenclatura adotados pelo catálogo.