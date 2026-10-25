---
name: databricks-sql-quality
description: Orienta boas práticas gerais de qualidade e revisão de SQL para Databricks. Use when criar, revisar, refatorar ou validar DDL e DML quanto a nomes, tipos, comentários e legibilidade.
---

# Qualidade de SQL Databricks

## Responsabilidade

Aplicar boas práticas de qualidade a SQL/DBSQL: nomenclatura clara, contrato de tipos, documentação e legibilidade. Se a empresa fornecer convenções próprias, trate-as como configuração do contexto; sem regras fornecidas, use recomendações gerais e não invente uma política corporativa.

## Quando não usar

- Não use para decidir a arquitetura, o tipo de objeto ou o ciclo de execução de um pipeline Lakeflow.
- Não use para orquestrar a migração de scripts PySpark ou gerar bundles completos.
- Não prometa um linter DBSQL ou auto-fix: essa ferramenta não está incluída no catálogo.

## Fluxo

1. Identifique as convenções explicitamente fornecidas no contexto; não presuma prefixos, domínios, schemas ou ferramentas internas.
2. Nomeie catálogo, schema, tabela e coluna com o substantivo principal no singular; siga a referência de naming para qualificadores e exceções.
3. Consulte as referências específicas antes de propor alterações de nomes, tipos, comentários ou estilo.
4. Escreva comentários de schema, tabela e coluna em linguagem do domínio, com contexto suficiente para interpretar granularidade, significado, unidades, filtros e nulos.
5. Preserve o significado dos dados; se a semântica de um nome ou regra não estiver clara, peça confirmação em vez de inferi-la.
6. Apresente exceções com justificativa e destaque mudanças que alterem o contrato publicado ou o comportamento da consulta.
7. Revise manualmente a legibilidade, a consistência e as referências; não trate conformidade estrutural como prova de equivalência de negócio.

## Referências

- [Nomenclatura de tabelas e views](references/table-naming.md)
- [Nomenclatura de colunas](references/column-naming.md)
- [Tipagem explícita](references/explicit-typing.md)
- [Documentação de metadados](references/metadata-documentation.md)
- [Legibilidade SQL](references/sql-readability.md)