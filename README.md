# TaskFlow-API
O TaskFlow é uma API para listas de tarefas desenvolvida para evidenciar excelência em engenharia de software. O projeto foca em infraestrutura e automação, utilizando CI/CD via GitHub Actions e Docker para assegurar testes automatizados e integração contínua.


# 🚀 TaskFlow API — Projeto CI/CD de Portfólio

[![CI/CD Pipeline](https://github.com/SEU-USUARIO/taskflow-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/SEU-USUARIO/taskflow-api/actions/workflows/ci-cd.yml)
[![Docker Hub](https://img.shields.io/docker/v/SEU-USUARIO/taskflow-api?label=Docker%20Hub&logo=docker)](https://hub.docker.com/r/SEU-USUARIO/taskflow-api)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> API REST em Python/Flask com pipeline CI/CD completo usando GitHub Actions e Docker.  
> Projeto desenvolvido para demonstrar boas práticas de DevOps em portfólio.

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Rodando com Docker](#-rodando-com-docker)
- [Testes](#-testes)
- [Como Funciona o CI/CD](#-como-funciona-o-cicd)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Endpoints da API](#-endpoints-da-api)

---

## 🎯 Sobre o Projeto

**TaskFlow API** é uma API REST para gerenciamento de tarefas (to-do list), construída com Flask.  
O foco principal do projeto é o **pipeline de CI/CD**, que demonstra:

- ✅ Lint automático de código
- ✅ Testes automatizados com cobertura mínima garantida
- ✅ Build e validação da imagem Docker
- ✅ Publicação automática no Docker Hub
- ✅ Deploy automático com notificações de status

---

## 🗂 Estrutura do Projeto

```
taskflow-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # 🔧 Pipeline CI/CD completo
├── src/
│   ├── __init__.py
│   └── app.py               # 🐍 Aplicação Flask
├── tests/
│   ├── __init__.py
│   └── test_app.py          # 🧪 Testes automatizados (pytest)
├── .dockerignore
├── .gitignore
├── Dockerfile               # 🐳 Multi-stage build
├── pyproject.toml           # ⚙️  Configuração pytest/cobertura
├── requirements.txt
└── README.md
```

---

## 💻 Como Rodar Localmente

### Pré-requisitos

- Python 3.12+
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/taskflow-api.git
cd taskflow-api

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
python src/app.py
```

A API estará disponível em `http://localhost:5000`.

---

## 🐳 Rodando com Docker

```bash
# Build da imagem
docker build -t taskflow-api .

# Executar o container
docker run -d \
  --name taskflow-api \
  -p 5000:5000 \
  -e APP_VERSION=1.0.0 \
  taskflow-api

# Ou via Docker Hub (após o CI/CD publicar)
docker run -d \
  -p 5000:5000 \
  SEU-USUARIO/taskflow-api:latest
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Cobertura mínima exigida: **80%**

O pipeline quebra automaticamente se a cobertura ficar abaixo desse limite.

---

## ⚙️ Como Funciona o CI/CD

O pipeline é acionado automaticamente em:
- **Push** nas branches `main` e `develop`
- **Pull Requests** para a branch `main`

### Fluxo Completo

```
Push/PR
   │
   ▼
┌─────────────────────┐
│  JOB 1: 🔍 Lint      │  Verifica estilo e bugs com Flake8
└──────────┬──────────┘
           │ (se passar)
           ▼
┌─────────────────────┐
│  JOB 2: 🧪 Testes   │  Pytest + cobertura ≥ 80% (falha = pipeline quebra)
└──────────┬──────────┘
           │ (se passar)
           ▼
┌─────────────────────┐
│  JOB 3: 🐳 Docker   │  Build + smoke test local do container
└──────────┬──────────┘
           │ (apenas branch main)
           ▼
┌─────────────────────┐
│  JOB 4: 📦 Push Hub │  Publica imagem com tag SHA + latest
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  JOB 5: 🚀 Deploy   │  Deploy em produção (SSH ou simulado)
└─────────────────────┘
```

### Configuração necessária

Adicione estes **Secrets** no repositório (Settings → Secrets → Actions):

| Secret | Descrição |
|--------|-----------|
| `DOCKERHUB_USERNAME` | Seu usuário no Docker Hub |
| `DOCKERHUB_TOKEN` | Access Token gerado no Docker Hub |

---

## 🌍 Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `PORT` | `5000` | Porta em que a aplicação escuta |
| `FLASK_DEBUG` | `false` | Ativa o modo debug do Flask |
| `APP_VERSION` | `1.0.0` | Versão exibida no health check |

---

## 🔌 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Health check |
| `GET` | `/tasks` | Lista todas as tarefas |
| `POST` | `/tasks` | Cria nova tarefa |
| `GET` | `/tasks/:id` | Busca tarefa por ID |
| `PATCH` | `/tasks/:id` | Atualiza tarefa |
| `DELETE` | `/tasks/:id` | Remove tarefa |

### Exemplos

```bash
# Health check
curl http://localhost:5000/

# Criar tarefa
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender CI/CD", "description": "GitHub Actions + Docker"}'

# Listar tarefas
curl http://localhost:5000/tasks

# Marcar como concluída
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Deletar tarefa
curl -X DELETE http://localhost:5000/tasks/1
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

<p align="center">
  Feito com ❤️ para demonstrar boas práticas de CI/CD
</p>
