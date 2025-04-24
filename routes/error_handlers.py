from flask import Blueprint, jsonify

error_bp = Blueprint("error_bp", __name__)

# Handle 404 errors (Page Not Found)
@error_bp.app_errorhandler(404)
def handle_404_error(e):
    return jsonify({"error": "Resource not found", "message": str(e)}), 404

# Handle 500 errors (Internal Server Error)
@error_bp.app_errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong"}), 500
