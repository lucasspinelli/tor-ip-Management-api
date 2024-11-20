from flask import Flask, request
import logging
from app.routes import bp as api_bp
from app.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    # Blueprints to separate rotes of auth and standard routes
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth', name='auth')


    #Application Logs
    @app.before_request
    def log_request_info():
        logging.info(
            f"Req Received: {request.method}{request.url}"
            f"Headers: {dict(request.headers)}"
            f"Body: {request.get_data(as_text=True)}"
        )

    @app.after_request
    def log_response_info(response):
        logging.info(
            f"Response sent: {request.method} {request.url} "
            f"Status: {response.status_code}"
        )
        return response
    return app
