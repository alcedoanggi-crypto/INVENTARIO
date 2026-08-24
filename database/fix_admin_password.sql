-- Ejecuta esto SOLO si ya importaste inventario_db.sql anteriormente
-- (con la contraseña en texto plano "admin123") y necesitas corregirla
-- para que funcione con el login de la app Flask.
--
-- Uso:
--   psql -U postgres -h localhost -d inventario_db -f database/fix_admin_password.sql
--
-- Deja al usuario "admin" con contraseña "admin" (hasheada con
-- pbkdf2:sha256, compatible con Werkzeug / Flask-Login).

UPDATE public."user"
SET password = 'pbkdf2:sha256:1000000$r6kOItqubuKe3Nc9$4563d4d94e844e7373c776d3ff69264b3ed2c3e75ebd5edb28a1126b32aee20f'
WHERE username = 'admin';
