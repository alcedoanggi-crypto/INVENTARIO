from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.extensions import db
from app.models import Department
from app.forms import DepartmentForm

departments_bp = Blueprint("departments", __name__)


@departments_bp.route("/")
@login_required
def list_departments():
    departments = Department.query.order_by(Department.name.asc()).all()
    department_form = DepartmentForm()
    return render_template(
        "departments/list.html",
        departments=departments,
        department_form=department_form,
    )


@departments_bp.route("/nuevo", methods=["POST"])
@login_required
def create_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(
            name=form.name.data.strip(),
            description=form.description.data,
        )
        db.session.add(department)
        db.session.commit()
        flash(f'Departamento "{department.name}" creado correctamente.', "success")
    else:
        flash("Error al crear el departamento. Revisa los datos ingresados.", "danger")

    return redirect(url_for("departments.list_departments"))


@departments_bp.route("/<int:department_id>/editar", methods=["POST"])
@login_required
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data.strip()
        department.description = form.description.data
        db.session.commit()
        flash(f'Departamento "{department.name}" actualizado correctamente.', "success")
    else:
        flash("Error al actualizar el departamento.", "danger")

    return redirect(url_for("departments.list_departments"))


@departments_bp.route("/<int:department_id>/eliminar", methods=["POST"])
@login_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    if department.categories:
        flash("No puedes eliminar un departamento que tiene categorías asociadas.", "danger")
        return redirect(url_for("departments.list_departments"))

    db.session.delete(department)
    db.session.commit()
    flash(f'Departamento "{department.name}" eliminado.', "info")
    return redirect(url_for("departments.list_departments"))
