from flask import Flask
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from dotenv import load_dotenv
from database import db
from routes.user_routes import user_bp  
from routes.task_routes import task_bp  
from routes.error_handlers import error_bp  

load_dotenv()

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api")  # Prefixes all user routes with `/api`
app.register_blueprint(task_bp, url_prefix="/api")  # Prefixes all task routes with `/api`
app.register_blueprint(error_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5003)
