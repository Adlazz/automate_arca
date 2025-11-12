import sqlite3
from typing import List, Tuple, Optional

class UsuarioDAO:
    def __init__(self, db_path: str = 'database/usuarios.db'):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def obtener_todos(self) -> List[Tuple]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()

    def buscar_por_nombre(self, nombre_parcial: str) -> List[Tuple]:
        nombre_parcial = f"%{nombre_parcial.lower()}%"
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE LOWER(nombre) LIKE ?", (nombre_parcial,))
            return cursor.fetchall()

    def insertar(self, nombre: str, cuit: str, cuit_retenido: str, password: str, password_atp: str = None) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nombre, cuit, cuit_retenido, password, password_atp)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, cuit, cuit_retenido, password, password_atp))
            conn.commit()

    def actualizar(self, nombre_usuario: str, campos: dict) -> None:
        if not campos:
            return
        query = "UPDATE usuarios SET " + ", ".join([f"{k} = ?" for k in campos]) + " WHERE nombre = ?"
        valores = list(campos.values()) + [nombre_usuario]
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()

    def eliminar_duplicados(self) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM usuarios
                WHERE id NOT IN (
                    SELECT MIN(id)
                    FROM usuarios
                    GROUP BY cuit
                )
            ''')
            conn.commit()
