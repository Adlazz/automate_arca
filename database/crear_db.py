import sqlite3

# Conectar a la base de datos (si no existe, se crea automáticamente)
conn = sqlite3.connect('database/usuarios.db')
cursor = conn.cursor()

# Crear la tabla 'usuarios'
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cuit TEXT NOT NULL,
    cuit_retenido TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tabla creadas correctamente.")