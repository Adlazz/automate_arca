import sqlite3

# Conectar a la base de datos (si no existe, se crea automáticamente)
conn = sqlite3.connect('database/usuarios.db')
cursor = conn.cursor()

# Crear la tabla 'usuarios' con nueva estructura
# Cambios:
# - nombre: Nombre del CONTRIBUYENTE (PJ o PF)
# - cuit: CUIT del CONTRIBUYENTE (quien presenta DDJJ)
# - cuit_representante: CUIT para login en ARCA (NULL si es PF que se representa a sí misma)
# - nombre_representante: Nombre del representante (NULL si es PF)
# - password: Password ARCA
# - password_atp: Password ATP
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cuit TEXT NOT NULL UNIQUE,
    cuit_representante TEXT,
    nombre_representante TEXT,
    password TEXT NOT NULL,
    password_atp TEXT
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tabla creadas correctamente.")