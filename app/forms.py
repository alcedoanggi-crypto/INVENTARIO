"""
Formularios (Flask-WTF) con validación del lado del servidor y
protección CSRF automática.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, TextAreaField, DecimalField,
    IntegerField, SelectField, RadioField, SubmitField
)
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Optional


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(max=150)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")


class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(max=150)])
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=4, message="Mínimo 4 caracteres")]
    )
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden")],
    )
    submit = SubmitField("Crear cuenta")


class DepartmentForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Descripción", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Guardar")


class CategoryForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Descripción", validators=[Optional(), Length(max=255)])
    department_id = SelectField("Departamento", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Guardar")


class ProductForm(FlaskForm):
    sku = StringField("SKU / Código", validators=[DataRequired(), Length(max=40)])
    name = StringField("Nombre del producto", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Descripción", validators=[Optional()])
    category_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    price = DecimalField("Precio unitario", validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField(
        "Cantidad inicial", validators=[DataRequired(), NumberRange(min=0)], default=0
    )
    min_stock = IntegerField(
        "Stock mínimo (alerta)", validators=[DataRequired(), NumberRange(min=0)], default=5
    )
    image = FileField(
        "Imagen del producto",
        validators=[FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "Solo se permiten imágenes")],
    )
    submit = SubmitField("Guardar producto")


class MovementForm(FlaskForm):
    product_id = SelectField("Producto", coerce=int, validators=[DataRequired()])
    movement_type = RadioField(
        "Tipo de movimiento",
        choices=[("entrada", "Entrada"), ("salida", "Salida")],
        default="entrada",
        validators=[DataRequired()],
    )
    quantity = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1)])
    reason = StringField("Motivo / referencia", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Registrar movimiento")
