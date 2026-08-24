from app.models import User


def test_listar_usuarios_autenticado(auth_client):
    response = auth_client.get("/admin/usuarios/")
    assert response.status_code == 200
    assert b"admin_test" in response.data


def test_crear_usuario(auth_client, app):
    response = auth_client.post("/admin/usuarios/nuevo", data={
        "username": "operador1",
        "email": "operador@test.com",
        "password": "password123",
        "role": "usuario"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"operador1" in response.data

    with app.app_context():
        user = User.query.filter_by(username="operador1").first()
        assert user is not None
        assert user.email == "operador@test.com"


def test_eliminar_usuario(auth_client, app):
    # Primero creamos un usuario
    auth_client.post("/admin/usuarios/nuevo", data={
        "username": "eliminar_me",
        "email": "eliminar@test.com",
        "password": "password123",
        "role": "usuario"
    })

    with app.app_context():
        user = User.query.filter_by(username="eliminar_me").first()
        user_id = user.id

    # Ejecutamos la eliminación
    response = auth_client.post(f"/admin/usuarios/eliminar/{user_id}", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        deleted_user = User.query.get(user_id)
        assert deleted_user is None