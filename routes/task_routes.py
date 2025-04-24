from flask import Blueprint, request
from database import db
from models.task import Task
from schemas import TaskSchema
from util import success_response, error_response

task_bp = Blueprint('task_bp', __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        errors = task_schema.validate(data)
        if errors:
            return error_response("Validation error", errors, 400)

        new_task = Task(**data)
        db.session.add(new_task)
        db.session.commit()

        return success_response("Task created successfully", task_schema.dump(new_task), 201)
    
    except Exception as e:
        return error_response("Internal server error", str(e), 500)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return success_response("Tasks retrieved", tasks_schema.dump(tasks))

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error_response("Task not found", None, 404)

    return success_response("Task retrieved", task_schema.dump(task))

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error_response("Task not found", None, 404)

    db.session.delete(task)
    db.session.commit()
    return success_response("Task deleted successfully", None)
