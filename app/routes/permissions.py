from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Role, Permission

permissions_bp = Blueprint("permissions", __name__)

@permissions_bp.route("/")
@login_required
def index():
    roles = Role.query.all()
    permissions = Permission.query.all()
    return render_template("admin/permissions.html", roles=roles, permissions=permissions)