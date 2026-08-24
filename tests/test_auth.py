def test_login_credenciales_correctas(client):
    # Intentar iniciar sesión con las credenciales registradas en la base de datos de prueba
    response = client.post("/login", data={
        "username": "admin_test",
        "password": "admin123"
    }, follow_redirects=True)

    # Validaciones
    assert response.status_code == 200
    # Confirma que ingresó al sistema verificando la presencia del nombre o elementos del dashboard
    assert b"admin_test" in response.data or b"Inventario Pro" in response.data