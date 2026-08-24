# Base de datos — importación

Este archivo (`inventario_db.sql`) es un dump completo de PostgreSQL:
crea la base de datos `inventario_db`, todas sus tablas, el trigger de
actualización automática de stock, y carga los datos de ejemplo
(incluyendo el usuario `admin`).

## Cómo importarlo

### Opción A — con psql (recomendado)

```bash
psql -U postgres -h localhost -f database/inventario_db.sql
```

Te pedirá la contraseña del usuario `postgres` de tu instalación local.
El script ya incluye `CREATE DATABASE inventario_db` y `\connect
inventario_db`, así que no necesitas crear la base de datos a mano
primero.

### Opción B — con pgAdmin

1. Abre pgAdmin y conéctate a tu servidor PostgreSQL.
2. Clic derecho sobre "Databases" → **Query Tool** (sin seleccionar una
   base de datos específica, para poder ejecutar el `CREATE DATABASE`).
3. Abre el archivo `inventario_db.sql` y ejecútalo completo (F5).

## Contraseña del usuario admin

El dump ya incluye la contraseña **hasheada** con `pbkdf2:sha256`
(compatible con Werkzeug/Flask-Login), lista para usarse:

- Usuario: `admin`
- Contraseña: `admin`

> Si ya habías importado una versión anterior de este dump (con la
> contraseña en texto plano `admin123`), corre
> `database/fix_admin_password.sql` para corregir esa fila sin tener
> que reimportar todo.

## Después de importar

Actualiza tu `.env` con la cadena de conexión real, por ejemplo:

```env
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/inventario_db
```

## ⚠️ Importante — pendiente antes de usar la app con esta base de datos

Este dump define una estructura **distinta** a la que actualmente usan
los modelos de la aplicación Flask (`app/models.py`). Por ejemplo:

- Las tablas se llaman `product`, `category`, `department`, `movement`,
  en vez de `products`, `categories`, etc.
- El stock vive en una tabla separada (`cantidades`), no como columna
  directa en `product`.
- `category` no está vinculada a `department` — el departamento solo
  se usa en `movement` (origen/destino de una transferencia).
- Los movimientos usan `'Entrada'` / `'Salida'` (con mayúscula) y un
  trigger de PostgreSQL recalcula el stock automáticamente.
- Hay tablas adicionales que el modelo actual no contempla: `supplier`
  y `foto`.

Por ahora solo el **login** (tabla `user`) quedó alineado con este
dump. El resto de los modelos y rutas (productos, categorías,
movimientos) todavía reflejan el diseño original y **no funcionarán
correctamente contra esta base de datos** hasta reescribirlos para que
calcen con este esquema real.
