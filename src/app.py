"""
This module takes care of starting the API Server,
Loading the DB, and Adding the endpoints
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Detect environment
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"

# Static build folder (React)
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')

# Initialize Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


# DATABASE CONFIG

db_url = os.getenv("DATABASE_URL")

if db_url:
    # Fix Heroku-style Postgres URLs
    db_url = db_url.replace("postgres://", "postgresql://")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    # Local fallback
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB & Migrate
db.init_app(app)
MIGRATE = Migrate(app, db, compare_type=True)


# JWT CONFIG

app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this!!"  # ← CAMBIA ESTO
jwt = JWTManager(app)


# ADMIN + CUSTOM COMMANDS

setup_admin(app)
setup_commands(app)


# API ROUTES

app.register_blueprint(api, url_prefix="/api")


# ERROR HANDLING

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# SITEMAP (DEV ONLY)

@app.route("/")
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, "index.html")


# SERVE REACT BUILD FILES

@app.route("/<path:path>", methods=["GET"])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = "index.html"
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0
    return response


# MAIN ENTRY POINT
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=PORT, debug=True)
