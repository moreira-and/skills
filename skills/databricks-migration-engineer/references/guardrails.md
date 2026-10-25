# Limites de segurança e execução

Estas regras são instruções ao agente. As permissões reais dependem do workspace e do Genie Code; o agente não deve contar com elas para se conter.

## Obrigatório

- Não faça deploy, commit nem push.
- Não aja em produção.
- Leia e valide apenas no workspace de teste.
- Peça confirmação explícita antes de ação destrutiva ou irreversível, mesmo no workspace de teste (apagar, sobrescrever, truncar, recriar objetos).
- Não exponha segredos, credenciais ou dados sensíveis em código, logs ou relatórios; mascare-os.
- Não declare execução ou validação real sem tê-la feito. Verificação estática e execução no workspace são coisas distintas e devem aparecer separadas no relatório.
- Em pedido de deploy, commit/push ou produção, recuse e indique que a ação é humana.

## Recomendado

- Prefira consultas de leitura e amostras pequenas na validação.
- Registre o que foi lido e executado para permitir revisão.
