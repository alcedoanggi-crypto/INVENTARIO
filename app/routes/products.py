import csv
import io
import os
import uuid

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    current_app, send_file
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Product, Category
from app.forms import ProductForm, MovementForm

products_bp = Blueprint("products", __name__)


def _save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(path)
    return unique_name


@products_bp.route("/")
@login_required
def list_products():
    query = Product.query.join(Category)

    search = request.args.get("q", "").strip()
    category_id = request.args.get("category_id", type=int)
    only_low_stock = request.args.get("low_stock") == "1"
    page = request.args.get("page", 1, type=int)

    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(Product.name.ilike(like), Product.sku.ilike(like)))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if only_low_stock:
        query = query.filter(Product.quantity <= Product.min_stock)

    pagination = query.order_by(Product.name.asc()).paginate(
        page=page, per_page=current_app.config["PRODUCTS_PER_PAGE"], error_out=False
    )

    categories = Category.query.order_by(Category.name.asc()).all()

    # Formulario para el modal de Nuevo Producto
    product_form = ProductForm()
    product_form.category_id.choices = [
        (c.id, f"{c.name} ({c.department.name})") for c in categories
    ]

    # Formulario para el modal de Movimientos
    movement_form = MovementForm()

    return render_template(
        "products/list.html",
        products=pagination.items,
        pagination=pagination,
        categories=categories,
        search=search,
        category_id=category_id,
        only_low_stock=only_low_stock,
        product_form=product_form,
        movement_form=movement_form,
    )


@products_bp.route("/exportar.csv")
@login_required
def export_csv():
    products = Product.query.join(Category).order_by(Product.name.asc()).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["SKU", "Nombre", "Categoría", "Departamento", "Precio", "Cantidad", "Stock mínimo", "Valor total"]
    )
    for p in products:
        writer.writerow(
            [
                p.sku, p.name, p.category.name if p.category else "",
                p.department.name if p.department else "",
                f"{p.price:.2f}", p.quantity, p.min_stock, f"{p.total_value:.2f}",
            ]
        )

    mem = io.BytesIO(buffer.getvalue().encode("utf-8-sig"))
    mem.seek(0)
    return send_file(
        mem, mimetype="text/csv", as_attachment=True,
        download_name="inventario.csv",
    )


@products_bp.route("/nuevo", methods=["POST"])
@login_required
def create_product():
    form = ProductForm()
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, f"{c.name} ({c.department.name})") for c in categories]

    if form.validate_on_submit():
        if Product.query.filter_by(sku=form.sku.data.strip()).first():
            flash("Ya existe un producto con ese SKU.", "danger")
            return redirect(url_for("products.list_products"))

        product = Product(
            sku=form.sku.data.strip(),
            name=form.name.data.strip(),
            description=form.description.data,
            category_id=form.category_id.data,
            price=form.price.data,
            quantity=form.quantity.data,
            min_stock=form.min_stock.data,
            image_filename=_save_image(form.image.data),
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Producto "{product.name}" creado correctamente.', "success")
    else:
        flash("Error al crear el producto. Revisa los datos ingresados.", "danger")

    return redirect(url_for("products.list_products"))


@products_bp.route("/<int:product_id>/editar", methods=["POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, f"{c.name} ({c.department.name})") for c in categories]

    if form.validate_on_submit():
        existing = Product.query.filter_by(sku=form.sku.data.strip()).first()
        if existing and existing.id != product.id:
            flash("Ya existe otro producto con ese SKU.", "danger")
            return redirect(url_for("products.list_products"))

        product.sku = form.sku.data.strip()
        product.name = form.name.data.strip()
        product.description = form.description.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.min_stock = form.min_stock.data

        new_image = _save_image(form.image.data)
        if new_image:
            product.image_filename = new_image

        db.session.commit()
        flash(f'Producto "{product.name}" actualizado correctamente.', "success")
    else:
        flash("Error al actualizar el producto.", "danger")

    return redirect(url_for("products.list_products"))


@products_bp.route("/<int:product_id>")
@login_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    movement_form = MovementForm()
    return render_template("products/detail.html", product=product, movement_form=movement_form)


@products_bp.route("/<int:product_id>/eliminar", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Producto "{name}" eliminado.', "info")
    return redirect(url_for("products.list_products"))