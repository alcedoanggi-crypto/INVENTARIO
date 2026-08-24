# 📦 Sistema de Gestión de Inventario Pro

Aplicación web full-stack para controlar productos, categorías,
departamentos y movimientos de stock en tiempo real — con dashboard
visual, kardex por producto, alertas de stock bajo, exportación a CSV
y una mini API REST.

Este proyecto demuestra habilidades de desarrollo backend con **Python y
Flask**, arquitectura limpia bajo el patrón **MVC** (Application Factory +
Blueprints), frontend dinámico con **Chart.js**, y manejo de bases de
datos relacionales con **PostgreSQL** (o SQLite para desarrollo local sin
configuración extra).

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?logo=chartdotjs&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📸 Vista Previa

> Agrega aquí 2-3 capturas de pantalla del sistema en funcionamiento.
>
> ```markdown
> ![Dashboard](docs/screenshots/dashboard.png)
> ![Listado de productos](docs/screenshots/productos.png)
> ![Kardex de producto](docs/screenshots/kardex.png)
> ```

**Demo en vivo:** _(agrega aquí el link si despliegas en Render/Railway)_
**Video demostrativo:** _(agrega aquí el link a tu video de TikTok/YouTube)_

---

## 🚀 Características Principales

- **Gestión multidimensional:** control de productos por categorías y
  departamentos, con relaciones bien normalizadas.
- **Dashboard visual:** KPIs de inventario (unidades totales, valor total,
  alertas) y gráficas interactivas con Chart.js — movimientos de los
  últimos 7 días y distribución de productos por departamento.
- **Movimientos de stock:** registro de entradas y salidas, con
  validación de stock disponible y **kardex** (historial completo) por
  producto.
- **Alertas de stock bajo:** cada producto define su propio umbral
  mínimo; el dashboard y el listado resaltan automáticamente lo que
  necesita reabastecimiento.
- **Autenticación segura:** login/registro con contraseñas hasheadas
  (Werkzeug) y protección CSRF (Flask-WTF) en todos los formularios.
- **Búsqueda y filtros:** por nombre, SKU, categoría o solo productos con
  stock bajo, con paginación.
- **Exportación a CSV** del inventario completo, un paso hacia la
  exportación a Excel/PDF planeada a futuro.
- **Manejo de archivos:** carga de imágenes de productos directamente al
  servidor, con nombres únicos para evitar colisiones.
- **API REST de solo lectura** (`/api/productos`) — primer paso hacia la
  integración con una app móvil.

## 🛠️ Tecnologías Utilizadas

| Categoría        | Tecnología                                          |
|-------------------|------------------------------------------------------|
| Backend           | Python 3.11 + Flask 3, Flask-Login, Flask-WTF        |
| Base de datos     | PostgreSQL (Flask-SQLAlchemy + Flask-Migrate)        |
| Frontend          | HTML5 (Jinja2), Bootstrap 5, Chart.js, JavaScript    |
| Seguridad         | Variables de entorno (python-dotenv), CSRF, hashing  |

## 📁 Estructura del Proyecto

Basado en un patrón de diseño profesional (MVC con Application Factory):

```
inventario_app/
├── app/
│   ├── __init__.py         # Application factory, registro de blueprints
│   ├── extensions.py       # Instancias de db, login_manager, csrf, migrate
│   ├── models.py           # User, Department, Category, Product, StockMovement
│   ├── forms.py            # Formularios WTForms con validación
│   ├── routes/              # Un blueprint por módulo funcional
│   │   ├── auth.py          # Login / registro / logout
│   │   ├── main.py          # Dashboard y métricas
│   │   ├── products.py      # CRUD de productos + export CSV + kardex
│   │   ├── categories.py    # CRUD de categorías
│   │   ├── departments.py   # CRUD de departamentos
│   │   ├── movements.py     # Registro e historial de movimientos
│   │   └── api.py           # API REST de solo lectura
│   ├── static/
│   │   ├── css/style.css    # Tema visual propio (no Bootstrap "de fábrica")
│   │   └── uploads/         # Imágenes de productos subidas por usuarios
│   └── templates/           # Vistas Jinja2 modulares por sección
├── config.py                 # Configuración segura basada en variables de entorno
├── requirements.txt           # Dependencias del proyecto
├── run.py                     # Punto de entrada de la aplicación
├── seed.py                    # Datos de prueba (usuario admin + catálogo demo)
└── .env.example                # Ejemplo de variables de entorno requeridas
```

---

## 🔧 Instalación y Uso Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/alcedoanggi-crypto/inventario_app.git
cd inventario_app
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/inventario_db
```

> 💡 **¿No tienes PostgreSQL instalado todavía?** Si omites `DATABASE_URL`,
> la aplicación usa automáticamente SQLite (`instance/inventario.db`), así
> puedes probar el proyecto sin instalar nada más.

### 5. Crear la base de datos y aplicar migraciones

```bash
flask db init      # solo la primera vez
flask db migrate -m "Estructura inicial"
flask db upgrade
```

> Alternativa rápida sin migraciones (crea las tablas directamente):
> `python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"`

### 6. Cargar datos de prueba (recomendado)

```bash
python seed.py
```

Esto crea un usuario administrador y un catálogo de ejemplo con
productos, categorías, departamentos y movimientos de los últimos 7 días
para que el dashboard se vea con datos reales desde el primer momento.

### 7. Ejecutar la aplicación

```bash
flask run
```

La aplicación estará disponible en `http://127.0.0.1:5000`

**Credenciales de prueba** (creadas por `seed.py`):
- Usuario: `admin`
- Contraseña: `admin`

> El primer usuario que se registre manualmente desde `/registro` también
> se vuelve administrador automáticamente.

---

## 🌐 Rutas principales

| Ruta                        | Descripción                                   |
|------------------------------|------------------------------------------------|
| `/login`, `/registro`        | Autenticación de usuarios (usuario + contraseña)|
| `/` (dashboard)               | KPIs, gráficas y alertas de stock bajo        |
| `/productos`                  | Listado, búsqueda, filtros y CSV export       |
| `/productos/<id>`             | Detalle de producto + kardex de movimientos   |
| `/categorias`, `/departamentos` | CRUD de catálogo                            |
| `/movimientos`                | Registro e historial de entradas/salidas      |
| `/api/productos`              | API REST de solo lectura (JSON)               |

---

## 🧪 Próximas Mejoras

- [ ] Tests automatizados con Pytest
- [ ] Exportación de reportes a Excel/PDF
- [ ] API REST de escritura (crear/editar productos) para app móvil
- [ ] Despliegue con Docker
- [ ] Notificaciones por correo cuando el stock cae por debajo del mínimo

## 👩‍💻 Autora

**Anggie Alcedo** — Ingeniera de Sistemas | Full Stack Developer & QA
Automation
[GitHub](https://github.com/alcedoanggi-crypto) ·
[LinkedIn](#) · alcedoanggi@gmail.com

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más
detalles.
