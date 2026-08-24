from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

from app.extensions import db
from app.models import StockMovement, Product
from app.forms import MovementForm

movements_bp = Blueprint("movements", __name__)


@movements_bp.route("/")
@login_required
def list_movements():
    page = request.args.get("page", 1, type=int)
    product_id = request.args.get("product_id", type=int)

    query = StockMovement.query
    if product_id:
        query = query.filter_by(product_id=product_id)

    pagination = query.order_by(StockMovement.created_at.desc()).paginate(
        page=page, per_page=current_app.config["MOVEMENTS_PER_PAGE"], error_out=False
    )

    form = MovementForm()
    form.product_id.choices = [
        (p.id, f"{p.sku} — {p.name} (Stock: {p.quantity})")
        for p in Product.query.order_by(Product.name.asc()).all()
    ]

    return render_template(
        "movements/list.html",
        movements=pagination.items,
        pagination=pagination,
        form=form,
    )


@movements_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def create_movement():
    form = MovementForm()
    form.product_id.choices = [
        (p.id, f"{p.sku} — {p.name} (Stock: {p.quantity})")
        for p in Product.query.order_by(Product.name.asc()).all()
    ]

    redirect_url = request.referrer or url_for("movements.list_movements")

    if not form.product_id.choices:
        flash("Primero debes crear al menos un producto.", "warning")
        return redirect(url_for("products.create_product"))

    if form.validate_on_submit():
        product = Product.query.get_or_404(form.product_id.data)

        if form.movement_type.data == StockMovement.SALIDA and form.quantity.data > product.quantity:
            flash(
                f'No hay stock suficiente. Disponible: {product.quantity} unidades de "{product.name}".',
                "danger",
            )
            return redirect(redirect_url)

        movement = StockMovement(
            product_id=product.id,
            movement_type=form.movement_type.data,
            quantity=form.quantity.data,
            reason=form.reason.data,
            user_id=current_user.id,
        )

        if form.movement_type.data == StockMovement.ENTRADA:
            product.quantity += form.quantity.data
        else:
            product.quantity -= form.quantity.data

        db.session.add(movement)
        db.session.commit()

        flash(
            f'¡Movimiento registrado con éxito! ({form.movement_type.data.capitalize()} de {form.quantity.data} unidades en "{product.name}").',
            "success",
        )
        return redirect(redirect_url)

    if request.method == "POST":
        flash("Ocurrió un error al procesar la solicitud. Revisa los datos ingresados.", "danger")

    return redirect(redirect_url)