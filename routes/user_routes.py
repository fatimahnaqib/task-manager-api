from flask import Blueprint, request
from database import db
from models.user import User
from schemas import UserSchema
from util import success_response, error_response
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return error_response("Validation error", errors, 400)

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return success_response("User created successfully", user_schema.dump(new_user), 201)
    
    except Exception as e:
        return error_response("Internal server error", str(e), 500)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return success_response("Users retrieved", users_schema.dump(users))

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", None, 404)

    return success_response("User retrieved", user_schema.dump(user))

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", None, 404)

    db.session.delete(user)
    db.session.commit()
    return success_response("User deleted successfully", None)

