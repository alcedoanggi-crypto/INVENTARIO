from datetime import datetime, timedelta

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models import Product, Category, Department, StockMovement

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    total_products = Product.query.count()
    total_departments = Department.query.count()
    total_categories = Category.query.count()

    total_units = db.session.query(func.coalesce(func.sum(Product.quantity), 0)).scalar()
    total_value = db.session.query(
        func.coalesce(func.sum(Product.quantity * Product.price), 0)
    ).scalar()

    # Carga de la lista completa de productos para la ventana modal
    products = Product.query.order_by(Product.name.asc()).all()

    low_stock_products = (
        Product.query.filter(Product.quantity <= Product.min_stock)
        .order_by(Product.quantity.asc())
        .limit(8)
        .all()
    )

    recent_movements = (
        StockMovement.query.order_by(StockMovement.created_at.desc()).limit(8).all()
    )

    # --- Datos para la gráfica: movimientos de los últimos 7 días ---
    today = datetime.utcnow().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    chart_labels = [d.strftime("%d/%m") for d in days]
    entradas_by_day = {d: 0 for d in days}
    salidas_by_day = {d: 0 for d in days}

    window_start = datetime.combine(days[0], datetime.min.time())
    recent_for_chart = StockMovement.query.filter(StockMovement.created_at >= window_start).all()
    for mv in recent_for_chart:
        day = mv.created_at.date()
        if day in entradas_by_day:
            if mv.movement_type == StockMovement.ENTRADA:
                entradas_by_day[day] += mv.quantity
            else:
                salidas_by_day[day] += mv.quantity

    chart_entradas = [entradas_by_day[d] for d in days]
    chart_salidas = [salidas_by_day[d] for d in days]

    # --- Distribución de productos por departamento ---
    dept_rows = (
        db.session.query(Department.name, func.count(Product.id))
        .join(Category, Category.department_id == Department.id)
        .join(Product, Product.category_id == Category.id)
        .group_by(Department.name)
        .all()
    )
    dept_labels = [row[0] for row in dept_rows] or ["Sin datos"]
    dept_values = [row[1] for row in dept_rows] or [1]

    return render_template(
        "dashboard.html",
        products=products,
        total_products=total_products,
        total_departments=total_departments,
        total_categories=total_categories,
        total_units=int(total_units or 0),
        total_value=float(total_value or 0),
        low_stock_products=low_stock_products,
        recent_movements=recent_movements,
        chart_labels=chart_labels,
        chart_entradas=chart_entradas,
        chart_salidas=chart_salidas,
        dept_labels=dept_labels,
        dept_values=dept_values,
    )