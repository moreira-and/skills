# Estrutura de Bundle para Migração

Os exemplos abaixo preservam a organização pretendida pelo material legado; são modelos configuráveis, não uma garantia de schema atual. Confirmar a versão da CLI, do bundle e do workspace antes do deploy.

## Layout ilustrativo

```text
sample_project/
├── databricks.yml
├── resources/
│   ├── jobs/               # Nome do diretório/coleção definido pelo bundle
│   └── pipelines/          # Nome do diretório/coleção definido pelo bundle
└── src/
    ├── 00_estatico/
    ├── 01_tracking/
    └── 02_transformacao/
```

Organização sugerida: prefixos numéricos (`00_reference`, `01_ingestion`, `02_transform`) podem indicar dependência; um arquivo SQL por objeto pode facilitar revisão; organizar recursos por etapa quando isso simplificar o grafo. Adaptar ao desenho do projeto. A regra de nomes singulares aplica-se aos identificadores de dados; não altere nomes de diretórios ou campos fixos exigidos pelo bundle.

## Configuração principal

O bundle normalmente separa nome do projeto, variáveis (catálogo, schema e tags), inclusão dos arquivos de recurso e targets de desenvolvimento/produção. Um esqueleto pode ter esta forma:

```yaml
bundle:
  name: sample-project

variables:
  catalog:
    description: Catálogo de destino
    default: dev_catalog
  schema:
    description: Schema de destino
    default: sample_schema

include:
  - resources/pipelines/*.pipeline.yml
  - resources/jobs/*.job.yml

targets:
  dev:
    mode: development
    default: true
    variables:
      catalog: dev_catalog
      schema: sample_schema
  prd:
    mode: production
    variables:
      catalog: prd_catalog
      schema: sample_schema
    run_as:
      service_principal_name: production-deployment-principal
```

Quando aplicável, tags podem incluir atributos genéricos de identificação do projeto e responsável. Confirmar interpolação, variáveis obrigatórias, modo, `run_as` e ambientes com a CLI/schema vigente. Substituir todos os placeholders por valores aprovados para o ambiente; nunca copiar credenciais de exemplo.

## Recurso de pipeline

Um recurso de pipeline declara destino, arquivos incluídos, modo e configuração específica. Confirmar suporte de cada campo na versão e workspace alvo; valores como serverless, channel e continuous não são universais.

```yaml
resources:
  pipelines:
    ingestion_pipeline:
      name: ${bundle.target}_ingestion
      catalog: ${var.catalog}
      schema: ${var.schema}
      serverless: true
      development: true
      continuous: false
      channel: PREVIEW
      libraries:
        - glob:
            include: src/01_ingestion/**
      configuration:
        input_path: /Volumes/sample_catalog/sample_schema/sample_volume/input/
```

Os valores `serverless`, `development`, `continuous`, `channel` e as chaves de configuração são exemplos do material legado; verificar se o target oferece suporte e substituir valores ilustrativos.

## Orquestração por job

Um job pode encadear recursos de pipeline por dependências declaradas. Trigger, condição, tempo mínimo entre execuções e identidade de execução precisam corresponder ao processo aprovado.

```yaml
resources:
  jobs:
    sample_job:
      name: ${bundle.target}_sample_job
      tasks:
        - task_key: ingestion
          pipeline_task:
            pipeline_id: ${resources.pipelines.ingestion_pipeline.id}
```

Para vários estágios, declarar tarefas e `depends_on` conforme o grafo aprovado, por exemplo `reference -> ingestion -> transform -> aggregate`. Um trigger de atualização de tabela e um schedule são alternativas, não defaults simultâneos; confirmar campos, expressões e timezone no schema atual do job.

## Conferência antes de gerar

- Confirmar catálogo/schema e acesso a fontes.
- Verificar suporte a recursos e campos na CLI/schema do ambiente.
- Confirmar identidade de execução para produção, trigger e configuração.
- Confirmar se o alvo aceita serverless e se o canal/runtime selecionado é permitido.
- Conferir nomes de recursos, interpolações de IDs e caminhos de inclusão.
- Validar o bundle no target apropriado quando a CLI e o ambiente estiverem disponíveis; relatar separadamente quando isso não puder ser executado.