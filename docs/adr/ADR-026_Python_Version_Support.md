# ADR-026: Python Version Support

- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A especificação ARCH-0006 definiu Python >=3.12 para o MVP. Porém, o ambiente de desenvolvimento local possui Python 3.11.9. O projeto sendo open source e um framework de aprendizado, a barreira de entrada para contribuidores deve ser baixa.
- **Decision:** Alterar o requisito mínimo para Python >=3.11. O pyproject.toml foi atualizado de `>=3.12` para `>=3.11`. Nenhuma feature do Python 3.12 é utilizada no código atual.
- **Consequences:** Maior compatibilidade com ambientes existentes. Mais usuários conseguem executar o projeto sem atualizar o Python. O código permanece compatível com 3.12+.
- **Hash:** `adr026-python-version-support-20260719`
