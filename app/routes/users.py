from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User, Role, AuditLog

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
@login_required
def list_users():
    users = User.query.all()
    roles = Role.query.all()
    return render_template("admin/users.html", users=users, roles=roles)


@users_bp.route("/nuevo", methods=["POST"])
@login_required
def create_user():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password")
    role = request.form.get("role", "usuario")

    if not username or not password:
        flash("El usuario y la contraseña son obligatorios.", "warning")
        return redirect(url_for("users.list_users"))

    if User.query.filter_by(username=username).first():
        flash("El nombre de usuario ya existe.", "danger")
        return redirect(url_for("users.list_users"))

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
    )
    db.session.add(new_user)

    # Registro en Auditoría
    log = AuditLog(
        user_id=current_user.id,
        action=f"Creación de usuario: {username}",
        module="Usuarios",
        ip_address=request.remote_addr,
    )
    db.session.add(log)

    db.session.commit()
    flash(f"Usuario '{username}' creado correctamente.", "success")
    return redirect(url_for("users.list_users"))


@users_bp.route("/editar/<int:user_id>", methods=["POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.email = request.form.get("email", "").strip()
    user.role = request.form.get("role", user.role)

    new_password = request.form.get("password")
    if new_password:
        user.password_hash = generate_password_hash(new_password)

    # Registro en Auditoría
    log = AuditLog(
        user_id=current_user.id,
        action=f"Actualización de usuario: {user.username}",
        module="Usuarios",
        ip_address=request.remote_addr,
    )
    db.session.add(log)

    db.session.commit()
    flash(f"Usuario '{user.username}' actualizado con éxito.", "info")
    return redirect(url_for("users.list_users"))


@users_bp.route("/eliminar/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash("No puedes eliminar tu propia cuenta en uso.", "warning")
        return redirect(url_for("users.list_users"))

    user = User.query.get_or_404(user_id)
    username = user.username
    db.session.delete(user)

    # Registro en Auditoría
    log = AuditLog(
        user_id=current_user.id,
        action=f"Eliminación de usuario: {username}",
        module="Usuarios",
        ip_address=request.remote_addr,
    )
    db.session.add(log)

    db.session.commit()
    flash(f"Usuario '{username}' eliminado correctamente.", "danger")
    return redirect(url_for("users.list_users"))

