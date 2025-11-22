import os
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from type_defs.http_types import HttpResponse
from utils.response_factory import error_response

load_dotenv()


def create_app():
    app = Flask(__name__)

    allowed_origins = os.getenv('ALLOWED_ORIGINS').split(',')

    CORS(app, origins=allowed_origins)

    from routes.jwt_routes import jwt_bp
    app.register_blueprint(jwt_bp, url_prefix="/jwt")

    @app.get("/health")
    def health_check() -> HttpResponse:
        return jsonify({"status": "OK"}), HTTPStatus.OK.value

    @app.errorhandler(Exception)
    def handle_validation_error(_: Exception):
        return error_response(
            message="Se produjo un error interno. Intente de nuevo más tarde.",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
