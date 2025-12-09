import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

usuarios = [
    ("GIMENEZ NATALIA KARINA", "23224869754", "30711019509", "Estudio2025", "Eliott7526"),
]

for nombre, cuit, cuit_retenido, password, password_atp in usuarios:
    dao.insertar(nombre, cuit, cuit_retenido, password, password_atp)

print("Datos insertados correctamente.")
