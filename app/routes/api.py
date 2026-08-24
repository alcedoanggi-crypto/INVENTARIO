"""
API REST de solo lectura para consulta de productos e inventario.
Devuelve JSON y reutiliza la sesión de usuario activa (Flask-Login).
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.extensions import db
from app.models import Product

api_bp = Blueprint("api", __name__)


def _product_to_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "description": p.description,
        "price": float(p.price) if p.price is not None else 0.0,
        "quantity": p.quantity,
        "min_stock": p.min_stock,
        "is_low_stock": p.is_low_stock,
        "category": p.category.name if p.category else None,
        "department": p.department.name if p.department else None,
        "image_url": f"/static/uploads/{p.image_filename}" if p.image_filename else None,
    }


@api_bp.route("/productos")
@login_required
def api_list_products():
    search = request.args.get("q", "").strip()
    stmt = db.select(Product)
    
    if search:
        like = f"%{search}%"
        stmt = stmt.where(Product.name.ilike(like) | Product.sku.ilike(like))
        
    products = db.session.scalars(stmt.order_by(Product.name.asc())).all()
    return jsonify([_product_to_dict(p) for p in products]), 200


@api_bp.route("/productos/<int:product_id>")
@login_required
def api_get_product(product_id: int):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
        
    return jsonify(_product_to_dict(product)), 200


@api_bp.route("/productos/stock-bajo")
@login_required
def api_low_stock():
    stmt = db.select(Product).where(Product.quantity <= Product.min_stock)
    products = db.session.scalars(stmt).all()
    return jsonify([_product_to_dict(p) for p in products]), 200