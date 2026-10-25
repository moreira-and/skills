# Modelo de relatório

Use as mesmas seções, na mesma ordem, em toda migração e em cada lote.

1. **Escopo**: o que foi tratado e o que ficou de fora.
2. **Inventário**: origens, destinos, chaves, ordenação, latência, consumidores, ambiente.
3. **Regras aplicadas**: cada decisão com o link da regra local usada.
4. **Divergências**: onde a regra local diferiu da prática geral e o que se seguiu.
5. **Premissas**: decisões tomadas sem regra local, com a justificativa.
6. **Itens não validados**: versão ou sintaxe sem confirmação e tudo o que só teve verificação estática.
7. **Riscos residuais**: impacto possível e responsável sugerido.
8. **Pendências do lote**: itens restantes e decisões necessárias.

Separe sempre "verificado estaticamente" de "executado no workspace de teste".
