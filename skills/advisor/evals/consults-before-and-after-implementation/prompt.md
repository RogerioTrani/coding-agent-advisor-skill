---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Preciso de um rate limiter de janela deslizante em Python (rate_limiter.py) que aguente várias threads batendo ao mesmo tempo, limite por chave de cliente, e com testes em pytest. Vai ser usado na frente de uma API de pagamentos, então não pode deixar passar requisição a mais.
