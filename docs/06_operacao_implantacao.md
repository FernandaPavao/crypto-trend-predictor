
---

## 6) `docs/06_operacao_implantacao.md` (rodar, docker, checklist release)
```markdown
# Operação & Implantação

## Pré-requisitos
- Python 3.10+
- (Opcional) Docker para Postgres.

## Ambiente
```bash
python -m venv .venv
# Linux/Mac: source .venv/bin/activate
# Windows:   .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # ajuste senhas/ports
