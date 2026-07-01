# Task Manager CLI

Gerenciador de tarefas em **Python puro + SQLite**, sem dependências externas.

## Arquitetura

```
main.py          ← CLI (apresentação)
src/
  config.py      ← configurações e caminhos
  models.py      ← entidades: Task, User, TaskStatus (Enum)
  database.py    ← conexão SQLite + criação das tabelas
  repository.py  ← CRUD: INSERT, SELECT, UPDATE, DELETE
  service.py     ← regras de negócio
tests/
  test_repository.py ← testes com banco em memória
```

**Fluxo:** `main.py → service.py → repository.py → SQLite`

## Como rodar

```bash
# Rodar o sistema
python3 main.py

# Rodar os testes
python3 -m pytest tests/ -v
```

## O que você aprende aqui

| Arquivo | Conceito |
|---|---|
| `models.py` | `@dataclass`, `Enum`, `@property`, `Optional` |
| `database.py` | `sqlite3`, context manager, DDL SQL |
| `repository.py` | CRUD completo em SQL, padrão Repository |
| `service.py` | `filter()`, `map()`, SRP, regras de negócio |
| `main.py` | `match/case`, `while True`, `try/except` |
| `tests/` | `unittest`, banco em memória, `assertRaises` |
