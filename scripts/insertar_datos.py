import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

usuarios = [
    ("PEREDO MONICA ISABEL", "27106230450", "27106230450", "Ramolaz2024"),
]

for nombre, cuit, cuit_retenido, password in usuarios:
    dao.insertar(nombre, cuit, cuit_retenido, password)

print("Datos insertados correctamente.")
