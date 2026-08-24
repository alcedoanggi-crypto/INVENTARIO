from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.extensions import db
from app.models import Category, Department
from app.forms import CategoryForm

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/")
@login_required
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    departments = Department.query.order_by(Department.name.asc()).all()

    category_form = CategoryForm()
    category_form.department_id.choices = [(d.id, d.name) for d in departments]

    return render_template(
        "categories/list.html",
        categories=categories,
        departments=departments,
        category_form=category_form,
    )


@categories_bp.route("/nueva", methods=["POST"])
@login_required
def create_category():
    form = CategoryForm()
    departments = Department.query.order_by(Department.name.asc()).all()
    form.department_id.choices = [(d.id, d.name) for d in departments]

    if not form.department_id.choices:
        flash("Primero debes crear al menos un departamento.", "warning")
        return redirect(url_for("departments.create_department"))

    if form.validate_on_submit():
        category = Category(
            name=form.name.data.strip(),
            description=form.description.data,
            department_id=form.department_id.data,
        )
        db.session.add(category)
        db.session.commit()
        flash(f'Categoría "{category.name}" creada correctamente.', "success")
    else:
        flash("Error al crear la categoría. Revisa los datos e intenta de nuevo.", "danger")

    return redirect(url_for("categories.list_categories"))


@categories_bp.route("/<int:category_id>/editar", methods=["POST"])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    departments = Department.query.order_by(Department.name.asc()).all()
    form.department_id.choices = [(d.id, d.name) for d in departments]

    if form.validate_on_submit():
        category.name = form.name.data.strip()
        category.description = form.description.data
        category.department_id = form.department_id.data
        db.session.commit()
        flash(f'Categoría "{category.name}" actualizada correctamente.', "success")
    else:
        flash("Error al actualizar la categoría.", "danger")

    return redirect(url_for("categories.list_categories"))


@categories_bp.route("/<int:category_id>/eliminar", methods=["POST"])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.products:
        flash("No puedes eliminar una categoría que tiene productos asociados.", "danger")
        return redirect(url_for("categories.list_categories"))
    db.session.delete(category)
    db.session.commit()
    flash("Categoría eliminada.", "info")
    return redirect(url_for("categories.list_categories"))
