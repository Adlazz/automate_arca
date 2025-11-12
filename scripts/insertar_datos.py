import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

usuarios = [
    ("VALLEJO GUSTAVO GERMAN", "20324892649", "20324892649", "Ramolaz2025", "Eliott7526"),
]

for nombre, cuit, cuit_retenido, password, password_atp in usuarios:
    dao.insertar(nombre, cuit, cuit_retenido, password, password_atp)

print("Datos insertados correctamente.")
