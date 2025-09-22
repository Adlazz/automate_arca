import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

# Actualizar CUIT para un usuario específico
dao.actualizar(
    nombre_usuario="LAZZARINI&LAZZARINI S.R.L.",
    campos={"cuit": "20146327401"}
)

print("CUIT actualizado correctamente.")