"""
ajustar_datos_post_migracion.py - Ajustes manuales después de migración

Corrige los nombres de personas jurídicas y sus representantes.
"""

import sqlite3

def ajustar_datos():
    conn = sqlite3.connect('database/usuarios.db')
    cursor = conn.cursor()

    try:
        print("=== AJUSTANDO DATOS POST-MIGRACIÓN ===\n")

        # Ajuste 1: GIMENEZ NATALIA KARINA → CONDOMINIO GIMENEZ KARINA NATALIA
        print("[1/2] Ajustando CONDOMINIO GIMENEZ KARINA NATALIA...")
        cursor.execute('''
            UPDATE usuarios
            SET nombre = 'CONDOMINIO GIMENEZ KARINA NATALIA',
                nombre_representante = 'GIMENEZ KARINA NATALIA'
            WHERE id = 1
        ''')
        print("  [OK] Nombre actualizado a: CONDOMINIO GIMENEZ KARINA NATALIA")
        print("  [OK] Representante actualizado a: GIMENEZ KARINA NATALIA")

        # Ajuste 2: LAZZARINI&LAZZARINI S.R.L. - nombre representante
        print("\n[2/2] Ajustando LAZZARINI&LAZZARINI S.R.L....")
        cursor.execute('''
            UPDATE usuarios
            SET nombre_representante = 'LAZZARINI JULIO OMAR'
            WHERE id = 4
        ''')
        print("  [OK] Representante actualizado a: LAZZARINI JULIO OMAR")

        conn.commit()

        print("\n[OK] Ajustes completados exitosamente\n")

        # Mostrar usuarios ajustados
        print("=== USUARIOS AJUSTADOS ===\n")
        cursor.execute("SELECT * FROM usuarios WHERE id IN (1, 4)")
        usuarios = cursor.fetchall()

        for u in usuarios:
            tipo = "PJ" if u[3] else "PF"
            print(f"ID: {u[0]} | Tipo: {tipo}")
            print(f"  Nombre: {u[1]}")
            print(f"  CUIT: {u[2]}")
            if u[3]:
                print(f"  Representante: {u[4]}")
                print(f"  CUIT Representante: {u[3]}")
            print()

    except Exception as e:
        conn.rollback()
        print(f"[X] Error durante los ajustes: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    ajustar_datos()
