# Implantação, Execução e Monitoramento

Lakeflow Declarative Pipelines é um recurso com ciclo de vida próprio. O SQL/Python que define o grafo não deve ser apresentado como job avulso que pode ser executado em qualquer SQL Warehouse ou notebook.

## Configuração e execução

- Um bundle pode definir o recurso de pipeline, bibliotecas/arquivos incluídos, catálogo/schema, modo de desenvolvimento, continuidade e configuração.
- Campos suportados, nomes, valores de canal e disponibilidade de serverless dependem da versão e do workspace. Validar schema do bundle no ambiente-alvo.
- Para orquestração, usar integração/task de pipeline suportada pelo job; não assumir que `spark.sql` ou task SQL/Python executa o ciclo de atualização do recurso.
- Para processos periódicos, distinguir atualização disparada da execução contínua; justificar custo de recurso ativo antes de recomendar modo contínuo.
- Alertar sobre impacto de mudanças de estado como migração entre estratégias SCD; alterações podem exigir recriação ou procedimento específico de atualização.

## Monitoramento

- Consultar métricas e eventos do pipeline para regras de qualidade, linhas, duração e falhas, conforme o workspace.
- Não tratar `print`/logs de notebook como fonte única de métricas do grafo declarativo.
- Confirmar nome/schema de tabelas de sistema e event log no ambiente; não inventar caminho universal.

## O que informar na entrega

1. O artefato gerado precisa estar registrado no recurso de pipeline correspondente.
2. A execução/deploy depende de bundle, permissões, configuração e ambiente compatíveis.
3. Separar validação local/estática de validação do bundle e execução real.
4. Registrar quaisquer campos, gatilhos, identidades de execução e parâmetros que ainda precisam de confirmação.

Não há uma configuração de bundle universal nesta referência; exemplos de `dabs-template.md` são configuráveis e dependentes de versão.