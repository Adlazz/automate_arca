import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO

dao = UsuarioDAO()

usuarios = dao.obtener_todos()

for usuario in usuarios:
    print(usuario)
