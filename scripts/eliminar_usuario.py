import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

# Nombre del usuario a eliminar
nombre_usuario = "NOMBRE DEL USUARIO A ELIMINAR"

if dao.eliminar(nombre_usuario):
    print(f"Usuario '{nombre_usuario}' eliminado correctamente.")
else:
    print(f"[X] No se encontró el usuario '{nombre_usuario}'.")
