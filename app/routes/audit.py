from flask import Blueprint, render_template
from flask_login import login_required
from app.models import AuditLog

audit_bp = Blueprint("audit", __name__)

@audit_bp.route("/")
@login_required
def index():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return render_template("admin/audit.html", logs=logs)