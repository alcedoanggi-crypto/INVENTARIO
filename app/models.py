"""
Definición de la estructura de la base de datos.

Entidades:
    User            -> usuarios que pueden iniciar sesión en el sistema
    Department      -> departamentos/áreas (ej. Electrónica, Hogar)
    Category        -> categorías dentro de un departamento
    Product         -> productos del inventario
    StockMovement   -> historial de entradas/salidas de stock (kardex)
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="usuario")

    movements = db.relationship("StockMovement", back_populates="user")

    def set_password(self, raw_password: str) -> None:
        # Se guarda el hash en el atributo 'password_hash' correspondiente a la columna
        self.password_hash = generate_password_hash(raw_password, method="pbkdf2:sha256")

    def check_password(self, raw_password: str) -> bool:
        # Se valida contra el atributo 'password_hash'
        return check_password_hash(self.password_hash, raw_password)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categories = db.relationship(
        "Category", back_populates="department", cascade="all, delete-orphan"
    )

    @property
    def product_count(self) -> int:
        return sum(len(c.products) for c in self.categories)

    def __repr__(self) -> str:
        return f"<Department {self.name}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department = db.relationship("Department", back_populates="categories")
    products = db.relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("name", "department_id", name="uq_category_name_department"),
    )

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(40), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock = db.Column(db.Integer, nullable=False, default=5)
    image_filename = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship("Category", back_populates="products")
    movements = db.relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="StockMovement.created_at.desc()",
    )

    @property
    def department(self):
        return self.category.department if self.category else None

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= self.min_stock

    @property
    def total_value(self):
        return (self.price or 0) * self.quantity

    def __repr__(self) -> str:
        return f"<Product {self.sku} - {self.name}>"


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    ENTRADA = "entrada"
    SALIDA = "salida"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    movement_type = db.Column(db.String(10), nullable=False)  # entrada | salida
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    product = db.relationship("Product", back_populates="movements")
    user = db.relationship("User", back_populates="movements")

    def __repr__(self) -> str:
        return f"<StockMovement {self.movement_type} {self.quantity} of product {self.product_id}>"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")