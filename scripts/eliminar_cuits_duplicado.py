import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()
dao.eliminar_duplicados()

print("Todos los registros duplicados eliminados correctamente.")
