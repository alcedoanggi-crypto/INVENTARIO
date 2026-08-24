import os
from flask import Flask, render_template

from config import config_by_name
from app.extensions import db, login_manager, csrf, migrate
from app.routes.users import users_bp
from app.routes.permissions import permissions_bp
from app.routes.audit import audit_bp


def create_app(config_name: str | None = None) -> Flask:
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    os.makedirs(app.instance_path, exist_ok=True)
    
    # Asignación segura de la carpeta de uploads para evitar KeyError en tests
    upload_folder = app.config.get("UPLOAD_FOLDER", os.path.join(app.root_path, "static", "uploads"))
    os.makedirs(upload_folder, exist_ok=True)

    # ---- extensiones ----
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ---- blueprints ----
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp
    from app.routes.departments import departments_bp
    from app.routes.movements import movements_bp
    from app.routes.api import api_bp
    from app.routes.reports import reports_bp
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/productos")
    app.register_blueprint(categories_bp, url_prefix="/categorias")
    app.register_blueprint(departments_bp, url_prefix="/departamentos")
    app.register_blueprint(movements_bp, url_prefix="/movimientos")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/reportes")
    # Registro dentro de create_app()
    app.register_blueprint(users_bp, url_prefix="/admin/usuarios")
    app.register_blueprint(permissions_bp, url_prefix="/admin/permisos")
    app.register_blueprint(audit_bp, url_prefix="/admin/auditoria")
    

    # ---- manejo de errores ----
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # ---- utilidades disponibles en todos los templates ----
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {"current_year": datetime.utcnow().year, "app_name": "Inventario Pro"}

    return app