"""
Testes automatizados para a TaskFlow API.
Cobre os principais fluxos de criação, leitura, atualização e exclusão de tarefas.
"""

import pytest
import sys
import os

# Garante que o módulo src/ seja encontrado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app


# ──────────────────────────────────────────────
# Fixture: cliente de teste Flask
# ──────────────────────────────────────────────

@pytest.fixture
def client():
    """Cria um cliente de teste com banco de dados limpo a cada teste."""
    app.config["TESTING"] = True
    # Limpa estado entre testes
    import app as app_module
    app_module.tasks.clear()
    app_module.task_counter = 1
    with app.test_client() as client:
        yield client


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────

def test_health_check(client):
    """Verifica se o endpoint raiz retorna status 200 e payload correto."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "TaskFlow API"
    assert "version" in data
    assert "timestamp" in data


# ──────────────────────────────────────────────
# Listagem de Tarefas
# ──────────────────────────────────────────────

def test_list_tasks_empty(client):
    """Lista vazia quando nenhuma tarefa foi criada."""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert data["tasks"] == []
    assert data["total"] == 0


def test_list_tasks_with_items(client):
    """Lista retorna tarefas após criação."""
    client.post("/tasks", json={"title": "Tarefa A"})
    client.post("/tasks", json={"title": "Tarefa B"})
    response = client.get("/tasks")
    data = response.get_json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


# ──────────────────────────────────────────────
# Criação de Tarefas
# ──────────────────────────────────────────────

def test_create_task_success(client):
    """Criação de tarefa com dados válidos."""
    response = client.post("/tasks", json={
        "title": "Estudar CI/CD",
        "description": "Aprender GitHub Actions"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["title"] == "Estudar CI/CD"
    assert data["description"] == "Aprender GitHub Actions"
    assert data["completed"] is False
    assert "created_at" in data


def test_create_task_without_title(client):
    """Criação falha sem o campo title."""
    response = client.post("/tasks", json={"description": "Sem título"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_task_empty_title(client):
    """Criação falha com título em branco."""
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_create_task_no_body(client):
    """Criação falha sem corpo na requisição."""
    response = client.post("/tasks", content_type="application/json", data="")
    assert response.status_code == 400


# ──────────────────────────────────────────────
# Busca de Tarefa por ID
# ──────────────────────────────────────────────

def test_get_task_success(client):
    """Busca de tarefa existente retorna dados corretos."""
    client.post("/tasks", json={"title": "Tarefa para buscar"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Tarefa para buscar"


def test_get_task_not_found(client):
    """Busca de tarefa inexistente retorna 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "error" in response.get_json()


# ──────────────────────────────────────────────
# Atualização de Tarefas
# ──────────────────────────────────────────────

def test_update_task_completed(client):
    """Marcar tarefa como concluída."""
    client.post("/tasks", json={"title": "Tarefa a concluir"})
    response = client.patch("/tasks/1", json={"completed": True})
    assert response.status_code == 200
    assert response.get_json()["completed"] is True


def test_update_task_title(client):
    """Atualizar título da tarefa."""
    client.post("/tasks", json={"title": "Título antigo"})
    response = client.patch("/tasks/1", json={"title": "Título novo"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Título novo"


def test_update_task_not_found(client):
    """Atualização de tarefa inexistente retorna 404."""
    response = client.patch("/tasks/999", json={"completed": True})
    assert response.status_code == 404


# ──────────────────────────────────────────────
# Exclusão de Tarefas
# ──────────────────────────────────────────────

def test_delete_task_success(client):
    """Exclusão de tarefa existente."""
    client.post("/tasks", json={"title": "Para deletar"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    # Confirma que não existe mais
    assert client.get("/tasks/1").status_code == 404


def test_delete_task_not_found(client):
    """Exclusão de tarefa inexistente retorna 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404


# ──────────────────────────────────────────────
# Fluxo Completo (integração)
# ──────────────────────────────────────────────

def test_full_task_lifecycle(client):
    """Teste de ciclo completo: criar → buscar → atualizar → deletar."""
    # Criar
    res = client.post("/tasks", json={"title": "Ciclo completo", "description": "Teste E2E"})
    assert res.status_code == 201
    task_id = res.get_json()["id"]

    # Buscar
    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200

    # Atualizar
    res = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert res.status_code == 200
    assert res.get_json()["completed"] is True

    # Deletar
    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 200

    # Confirmar ausência
    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 404
