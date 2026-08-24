import psycopg2

try:
    conn = psycopg2.connect(
        dbname="inventario_db",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432",
    )
    print("\n✅ ¡CONEXIÓN EXITOSA A POSTGRESQL!\n")
    conn.close()
except Exception as e:
    print("\n❌ FALLÓ LA CONEXIÓN.")
    print("Detalle técnico del error:", repr(e))