"""
Carga datos de prueba: usuario admin, departamentos, categorías,
productos y algunos movimientos de stock.

Uso:
    python seed.py
"""
import random
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import User, Department, Category, Product, StockMovement

app = create_app()

DEPARTMENTS = {
    "Electrónica": ["Computadoras", "Celulares", "Audio"],
    "Hogar": ["Cocina", "Muebles"],
    "Oficina": ["Papelería", "Mobiliario"],
}

PRODUCTS = [
    # (sku, nombre, categoría, precio, cantidad, min_stock)
    ("ELEC-001", "Laptop 14'' 16GB RAM", "Computadoras", 899.99, 12, 5),
    ("ELEC-002", "Mouse inalámbrico", "Computadoras", 19.99, 45, 10),
    ("ELEC-003", "Teléfono gama media", "Celulares", 259.00, 8, 5),
    ("ELEC-004", "Audífonos bluetooth", "Audio", 49.90, 3, 8),
    ("ELEC-005", "Parlante portátil", "Audio", 39.50, 20, 6),
    ("HOG-001", "Licuadora 600W", "Cocina", 34.99, 15, 5),
    ("HOG-002", "Juego de sartenes", "Cocina", 59.90, 2, 5),
    ("HOG-003", "Silla reclinable", "Muebles", 129.00, 6, 3),
    ("OFI-001", "Resma de papel bond", "Papelería", 4.50, 100, 20),
    ("OFI-002", "Silla ergonómica", "Mobiliario", 149.00, 4, 4),
]


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(username="admin", role="admin")
        admin.set_password("admin")
        db.session.add(admin)

        category_lookup = {}
        for dept_name, cat_names in DEPARTMENTS.items():
            dept = Department(name=dept_name, description=f"Departamento de {dept_name.lower()}")
            db.session.add(dept)
            db.session.flush()
            for cat_name in cat_names:
                cat = Category(name=cat_name, department_id=dept.id)
                db.session.add(cat)
                db.session.flush()
                category_lookup[cat_name] = cat.id

        db.session.flush()

        products_by_sku = {}
        for sku, name, cat_name, price, qty, min_stock in PRODUCTS:
            product = Product(
                sku=sku, name=name, category_id=category_lookup[cat_name],
                price=price, quantity=qty, min_stock=min_stock,
                description=f"{name} — producto de demostración.",
            )
            db.session.add(product)
            db.session.flush()
            products_by_sku[sku] = product

        db.session.flush()

        # movimientos de ejemplo en los últimos 7 días
        random.seed(42)
        now = datetime.utcnow()
        for i in range(25):
            product = random.choice(list(products_by_sku.values()))
            mv_type = random.choice([StockMovement.ENTRADA, StockMovement.SALIDA])
            qty = random.randint(1, 6)
            mv = StockMovement(
                product_id=product.id,
                movement_type=mv_type,
                quantity=qty,
                reason="Movimiento de demostración",
                user_id=admin.id,
                created_at=now - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23)),
            )
            db.session.add(mv)

        db.session.commit()
        print("✅ Datos de prueba cargados correctamente.")
        print("   Usuario: admin")
        print("   Contraseña: admin")


if __name__ == "__main__":
    run()
