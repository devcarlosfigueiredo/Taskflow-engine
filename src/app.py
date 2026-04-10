"""
TaskFlow API - Uma API REST simples para gerenciamento de tarefas.
Demonstra boas práticas de desenvolvimento Python com CI/CD.
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Simulação de banco de dados em memória
tasks = {}
task_counter = 1

# ──────────────────────────────────────────────
# Rotas da API
# ──────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health_check():
    """Endpoint de health check — usado pelo CI/CD para verificar o deploy."""
    return jsonify({
        "status": "ok",
        "service": "TaskFlow API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """Retorna todas as tarefas cadastradas."""
    return jsonify({
        "tasks": list(tasks.values()),
        "total": len(tasks)
    }), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Cria uma nova tarefa."""
    global task_counter

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Campo 'title' é obrigatório"}), 400

    title = data["title"].strip()
    if not title:
        return jsonify({"error": "O título não pode ser vazio"}), 400

    task = {
        "id": task_counter,
        "title": title,
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    tasks[task_counter] = task
    task_counter += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Busca uma tarefa específica pelo ID."""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    """Atualiza o status de conclusão de uma tarefa."""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404

    data = request.get_json() or {}
    if "completed" in data:
        task["completed"] = bool(data["completed"])
    if "title" in data and data["title"].strip():
        task["title"] = data["title"].strip()
    if "description" in data:
        task["description"] = data["description"]

    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Remove uma tarefa pelo ID."""
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    return jsonify({"message": f"Tarefa {task_id} removida com sucesso"}), 200


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
