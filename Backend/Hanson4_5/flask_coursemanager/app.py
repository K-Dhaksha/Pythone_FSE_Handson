from flask import Flask
from courses.routes import courses_bp
from config import Config
from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from extensions import db, migrate



def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    Migrate(app, db)  
    from courses import models
    from courses.routes import courses_bp  
    app.register_blueprint(courses_bp)
    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "status":"error",
            "message":"Resource not found"
        }),404


    @app.errorhandler(500)
    def server_error(error):

        return jsonify({
            "status":"error",
            "message":"Internal Server Error"
        }),500
    return app



app = create_app()


if __name__ == "__main__":
    app.run()