"""
migrar_db_personas_juridicas.py - Script de migración de base de datos

Cambios:
- Renombra 'cuit' a 'cuit_representante' (CUIT usado para login)
- Renombra 'cuit_retenido' a 'cuit' (CUIT del contribuyente principal)
- Agrega columna 'nombre_representante' (nombre de quien hace login)

Estructura nueva:
- nombre: Nombre del CONTRIBUYENTE (PJ o PF)
- cuit: CUIT del CONTRIBUYENTE (quien presenta DDJJ)
- cuit_representante: CUIT para login en ARCA (NULL si es PF que se representa a sí misma)
- nombre_representante: Nombre del representante (NULL si es PF)
- password: Password ARCA
- password_atp: Password ATP
"""

import sqlite3
import os
import shutil
from datetime import datetime

def migrar_base_datos(db_path='database/usuarios.db'):
    # Crear backup
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    print(f"[OK] Backup creado: {backup_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Crear tabla temporal con nueva estructura
        cursor.execute('''
        CREATE TABLE usuarios_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cuit TEXT NOT NULL UNIQUE,
            cuit_representante TEXT,
            nombre_representante TEXT,
            password TEXT NOT NULL,
            password_atp TEXT
        )
        ''')
        print("[OK] Tabla temporal creada")

        # 2. Obtener datos de la tabla original
        cursor.execute("SELECT id, nombre, cuit, cuit_retenido, password, password_atp FROM usuarios")
        usuarios_old = cursor.fetchall()

        # 3. Migrar datos a nueva estructura
        for usuario in usuarios_old:
            id_old, nombre, cuit_old, cuit_retenido, password, password_atp = usuario

            # Lógica de migración:
            # - El 'cuit_retenido' pasa a ser el 'cuit' principal (el contribuyente)
            # - El 'cuit' anterior pasa a ser 'cuit_representante'
            # - Si cuit == cuit_retenido, entonces es persona física (representante NULL)

            if cuit_old == cuit_retenido:
                # Persona física que se representa a sí misma
                nuevo_cuit = cuit_retenido
                nuevo_cuit_representante = None
                nuevo_nombre_representante = None
            else:
                # Persona jurídica con representante
                nuevo_cuit = cuit_retenido
                nuevo_cuit_representante = cuit_old
                # Por defecto, asumimos que el nombre es del representante
                # Esto habrá que ajustarlo manualmente después
                nuevo_nombre_representante = f"REPRESENTANTE DE {nombre}"

            cursor.execute('''
                INSERT INTO usuarios_new
                (nombre, cuit, cuit_representante, nombre_representante, password, password_atp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, nuevo_cuit, nuevo_cuit_representante, nuevo_nombre_representante, password, password_atp))

            print(f"[OK] Migrado: {nombre} - CUIT: {nuevo_cuit}")

        # 4. Eliminar tabla original
        cursor.execute("DROP TABLE usuarios")
        print("[OK] Tabla original eliminada")

        # 5. Renombrar tabla nueva
        cursor.execute("ALTER TABLE usuarios_new RENAME TO usuarios")
        print("[OK] Tabla renombrada")

        conn.commit()
        print("\n[OK] Migración completada exitosamente")
        print(f"[INFO] Si algo salió mal, restaurá desde: {backup_path}")

        # 6. Mostrar tabla migrada
        cursor.execute("SELECT * FROM usuarios")
        usuarios_migrados = cursor.fetchall()

        print("\n=== USUARIOS MIGRADOS ===")
        for u in usuarios_migrados:
            print(f"\nID: {u[0]}")
            print(f"  Nombre: {u[1]}")
            print(f"  CUIT: {u[2]}")
            print(f"  CUIT Representante: {u[3] or '(N/A - Persona Física)'}")
            print(f"  Nombre Representante: {u[4] or '(N/A)'}")

        print("\n[IMPORTANTE] Revisá los datos migrados y ajustá manualmente:")
        print("  1. Los nombres de representantes (actualmente genéricos)")
        print("  2. Los nombres de contribuyentes (pueden ser PJ, no PF)")

    except Exception as e:
        conn.rollback()
        print(f"\n[X] Error durante la migración: {e}")
        print(f"[INFO] Restaurá el backup: {backup_path}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== MIGRACIÓN DE BASE DE DATOS - PERSONAS JURÍDICAS ===\n")

    respuesta = input("¿Querés continuar con la migración? (S/N): ").strip().upper()
    if respuesta != "S":
        print("[X] Migración cancelada")
        exit()

    migrar_base_datos()
