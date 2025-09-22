import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

# Modificar los datos de un usuario existente
dao.actualizar(
    nombre_usuario="LAZZARINI HECTOR CESAR",
    campos={"password": "Ramolaz2025"}
)

print("Datos del usuario modificados correctamente.")
