---
name: pyspark-to-lakeflow
description: Conduz a migração de pipelines PySpark imperativos para Lakeflow SQL e DAB, preservando comportamento e rastreabilidade. Use when inventariar, converter ou validar um fluxo legado.
---

# Migração PySpark para Lakeflow

## Responsabilidade

Conduzir a migração de scripts PySpark imperativos para pipelines declarativos Lakeflow, com inventário, decisões aprovadas, produção de artefatos e validação de equivalência. Esta skill coordena o processo; não substitui as referências técnicas específicas de SQL, Lakeflow ou DAB.

## Quando não usar

- Não use para criar um pipeline novo sem código legado a migrar.
- Não use como guia isolado de estilo DBSQL ou de operação contínua de um pipeline existente.
- Não transforme conversões sintáticas em equivalência de negócio presumida.

## Fluxo

1. Inventarie scripts, fontes, destinos, dependências, regras de negócio e padrões imperativos; registre cobertura e pendências.
2. Proponha o mapeamento de nomes, objetos declarativos e bloqueios. Use nomes singulares para catálogo, schema, tabela e coluna; aguarde aprovação antes de mudar um identificador existente que afete contratos ou consumidores.
3. Converta transformações preservando regras, tipos, tratamento de nulos, desempates, chaves, sequenciamento e comportamento incremental; documente qualquer diferença.
4. Organize SQL e configurações de bundle conforme os exemplos e limites de versão aplicáveis, sem tratar templates como configurações universais.
5. Valide referências, artefatos, lógica e conteúdo estático; registre evidência de versão ou marque a compatibilidade como não validada.
6. Entregue mapa de proveniência, decisões aprovadas, pendências e manifesto de validação; não declare deploy validado sem executar a verificação correspondente no ambiente-alvo.

## Referências

- [Padrões de conversão](references/conversion-patterns.md)
- [Estrutura de bundle](references/dabs-template.md)
- [Checklist e manifesto](references/validation-checklist.md)