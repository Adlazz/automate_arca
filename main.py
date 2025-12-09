"""main.py - Menú maestro para seleccionar usuario y operación a automatizar."""

from database.dao.usuario_dao import UsuarioDAO
import sqlite3
import sys
import os

dao = UsuarioDAO()

def seleccionar_usuario():
    usuarios = dao.obtener_todos()
    if not usuarios:
        print("[X] No hay usuarios disponibles en la base de datos.")
        return None

    nombre_parcial = input("> Ingrese parte del nombre del usuario: ").strip().lower()
    coincidencias = dao.buscar_por_nombre(nombre_parcial)

    if not coincidencias:
        print("[X] No se encontraron coincidencias.")
        return None

    print("\n- Usuarios encontrados:")
    for i, u in enumerate(coincidencias):
        print(f"{i + 1}. {u[1]} - {u[2]}")

    try:
        seleccion = int(input("\nSeleccione el número correspondiente: ")) - 1
        if 0 <= seleccion < len(coincidencias):
            return coincidencias[seleccion]
        else:
            print("[X] Selección inválida.")
            return None
    except ValueError:
        print("[X] Por favor ingrese un número válido.")
        return None

def ejecutar_portal_iva(usuario, periodo, tipo_operacion):
    """Ejecuta la automatización del Portal IVA."""
    try:
        from automatizaciones.portal_iva import login_afip
        nombre = usuario[1]
        cuit = usuario[2]
        password = usuario[4]
        login_afip(cuit, password, periodo, tipo_operacion, nombre)
    except ImportError as e:
        print(f"[X] Error al importar el módulo portal_iva: {e}")
    except Exception as e:
        print(f"[X] Error al ejecutar Portal IVA: {e}")

def ejecutar_consulta_retenciones(usuario, fecha_desde, fecha_hasta):
    """Ejecuta la automatización de consulta de retenciones."""
    try:
        from automatizaciones.consultar_retenciones import login_afip
        nombre, cuit, cuit_retenido, password = usuario[1], usuario[2], usuario[3], usuario[4]
        login_afip(cuit, cuit_retenido, password, fecha_desde, fecha_hasta, nombre)
    except ImportError as e:
        print(f"[X] Error al importar el módulo consultar_retenciones: {e}")
    except Exception as e:
        print(f"[X] Error al ejecutar consulta de retenciones: {e}")

def ejecutar_ddjj_atp(usuario, periodo, base_imponible):
    """Ejecuta la automatización de DDJJ ATP (Rentas Formosa)."""
    try:
        from automatizaciones.ddjj_atp import login_afip
        nombre = usuario[1]
        cuit = usuario[2]
        password_atp = usuario[5] if len(usuario) > 5 and usuario[5] else usuario[4]
        login_afip(cuit, password_atp, periodo, base_imponible, nombre)
    except ImportError as e:
        print(f"[X] Error al importar el módulo ddjj_atp: {e}")
    except Exception as e:
        print(f"[X] Error al ejecutar DDJJ ATP: {e}")

def menu_automatizaciones():
    """Menú de automatizaciones (operaciones AFIP)."""
    usuario = seleccionar_usuario()
    if not usuario:
        return

    print(f"\n[OK] Usuario seleccionado: {usuario[1]} - {usuario[2]}")
    print("\nSeleccione la acción a realizar:")
    print("1. Consultar Retenciones")
    print("2. Presentar Libro IVA")
    print("3. Presentar DDJJ ATP")
    print("0. Volver al menú principal")

    opcion = input("\nIngrese opción (0, 1, 2 o 3): ").strip()

    if opcion == "1":
        fecha_desde = input("Ingrese Fecha Desde (DDMMYYYY): ")
        fecha_hasta = input("Ingrese Fecha Hasta (DDMMYYYY): ")

        if not validar_fecha(fecha_desde) or not validar_fecha(fecha_hasta):
            print("[X] Formato de fecha inválido. Use DDMMYYYY")
            return

        ejecutar_consulta_retenciones(usuario, fecha_desde, fecha_hasta)

    elif opcion == "2":
        periodo = input("Ingrese el período fiscal (formato MM/YYYY): ")
        if not validar_periodo(periodo):
            print("[X] Formato de período inválido. Use MM/YYYY")
            return

        tipo = input("Tipo de operación: [N] Ninguna / [E] Exentas: ").strip().upper()
        if tipo not in ["N", "E"]:
            print("[X] Tipo de operación inválido. Use N o E.")
            return

        tipo_operacion = "ninguna" if tipo == "N" else "exentas"
        ejecutar_portal_iva(usuario, periodo, tipo_operacion)

    elif opcion == "3":
        periodo = input("Ingrese el período fiscal (formato MM/YYYY): ")
        if not validar_periodo(periodo):
            print("[X] Formato de período inválido. Use MM/YYYY")
            return

        base_imponible = input("Ingrese la Base Imponible (use punto como separador decimal, ej: 999.99): ")
        if not validar_base_imponible(base_imponible):
            print("[X] Formato de Base Imponible inválido. Use solo números y punto decimal.")
            return

        ejecutar_ddjj_atp(usuario, periodo, base_imponible)

    elif opcion == "0":
        return

    else:
        print("[X] Opción inválida.")

def menu_gestion_bd():
    """Menú de gestión de base de datos."""
    while True:
        print("\n=== Gestión de Base de Datos ===")
        print("1. Insertar nuevo usuario")
        print("2. Consultar usuarios")
        print("3. Modificar datos de usuario")
        print("4. Actualizar CUIT de usuario")
        print("5. Eliminar usuario")
        print("0. Volver al menú principal")

        opcion = input("\nIngrese opción: ").strip()

        if opcion == "1":
            insertar_usuario()
        elif opcion == "2":
            consultar_usuarios()
        elif opcion == "3":
            modificar_usuario()
        elif opcion == "4":
            actualizar_cuit_usuario()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "0":
            break
        else:
            print("[X] Opción inválida.")

def insertar_usuario():
    """Inserta un nuevo usuario en la base de datos."""
    print("\n--- Insertar Nuevo Usuario ---")
    nombre = input("Nombre completo: ").strip().upper()
    cuit = input("CUIT: ").strip()
    cuit_retenido = input("CUIT Retenido: ").strip()
    password = input("Password AFIP: ").strip()
    password_atp = input("Password ATP (presione Enter si es igual a AFIP): ").strip()

    if not password_atp:
        password_atp = None

    try:
        dao.insertar(nombre, cuit, cuit_retenido, password, password_atp)
        print("[OK] Usuario insertado correctamente.")
    except sqlite3.IntegrityError:
        print("[X] Error: Ya existe un usuario con ese CUIT retenido.")
    except Exception as e:
        print(f"[X] Error al insertar usuario: {e}")

def consultar_usuarios():
    """Consulta y muestra todos los usuarios."""
    print("\n--- Lista de Usuarios ---")
    usuarios = dao.obtener_todos()
    if not usuarios:
        print("[X] No hay usuarios en la base de datos.")
        return

    for u in usuarios:
        password_atp_display = u[5] if len(u) > 5 and u[5] else "(igual a AFIP)"
        print(f"ID: {u[0]} | Nombre: {u[1]} | CUIT: {u[2]} | CUIT Ret: {u[3]} | Pass ATP: {password_atp_display}")

def modificar_usuario():
    """Modifica datos de un usuario existente."""
    print("\n--- Modificar Usuario ---")
    nombre = input("Nombre del usuario a modificar: ").strip().upper()

    print("\n¿Qué desea modificar?")
    print("1. Password AFIP")
    print("2. Password ATP")
    print("3. CUIT Retenido")
    print("4. Todos los campos")

    opcion = input("\nIngrese opción: ").strip()
    campos = {}

    if opcion == "1":
        campos["password"] = input("Nuevo password AFIP: ").strip()
    elif opcion == "2":
        password_atp = input("Nuevo password ATP: ").strip()
        campos["password_atp"] = password_atp if password_atp else None
    elif opcion == "3":
        campos["cuit_retenido"] = input("Nuevo CUIT Retenido: ").strip()
    elif opcion == "4":
        campos["password"] = input("Nuevo password AFIP: ").strip()
        password_atp = input("Nuevo password ATP (Enter para dejar vacío): ").strip()
        campos["password_atp"] = password_atp if password_atp else None
        campos["cuit_retenido"] = input("Nuevo CUIT Retenido: ").strip()
    else:
        print("[X] Opción inválida.")
        return

    try:
        dao.actualizar(nombre, campos)
        print("[OK] Usuario actualizado correctamente.")
    except Exception as e:
        print(f"[X] Error al actualizar usuario: {e}")

def actualizar_cuit_usuario():
    """Actualiza el CUIT de un usuario."""
    print("\n--- Actualizar CUIT ---")
    nombre = input("Nombre del usuario: ").strip().upper()
    nuevo_cuit = input("Nuevo CUIT: ").strip()

    try:
        dao.actualizar(nombre, {"cuit": nuevo_cuit})
        print("[OK] CUIT actualizado correctamente.")
    except Exception as e:
        print(f"[X] Error al actualizar CUIT: {e}")

def eliminar_usuario():
    """Elimina un usuario de la base de datos."""
    print("\n--- Eliminar Usuario ---")
    nombre_parcial = input("Ingrese parte del nombre del usuario a eliminar: ").strip().lower()
    coincidencias = dao.buscar_por_nombre(nombre_parcial)

    if not coincidencias:
        print("[X] No se encontraron coincidencias.")
        return

    print("\n- Usuarios encontrados:")
    for i, u in enumerate(coincidencias):
        print(f"{i + 1}. {u[1]} - CUIT: {u[2]}")

    try:
        seleccion = int(input("\nSeleccione el número del usuario a eliminar (0 para cancelar): ")) - 1
        if seleccion == -1:
            print("[X] Operación cancelada.")
            return
        if 0 <= seleccion < len(coincidencias):
            usuario = coincidencias[seleccion]
            nombre_completo = usuario[1]

            confirmacion = input(f"\n¿Está seguro de eliminar '{nombre_completo}' - CUIT: {usuario[2]}? (S/N): ").strip().upper()
            if confirmacion != "S":
                print("[X] Operación cancelada.")
                return

            if dao.eliminar(nombre_completo):
                print("[OK] Usuario eliminado correctamente.")
            else:
                print(f"[X] Error: No se pudo eliminar el usuario.")
        else:
            print("[X] Selección inválida.")
    except ValueError:
        print("[X] Por favor ingrese un número válido.")
    except Exception as e:
        print(f"[X] Error al eliminar usuario: {e}")

def main():
    """Función principal del menú."""
    while True:
        print("\n" + "=" * 50)
        print("=== Automatización ARCA - Menú Principal ===")
        print("=" * 50)
        print("1. Ejecutar Automatizaciones AFIP")
        print("2. Gestión de Base de Datos")
        print("0. Salir del programa")

        opcion = input("\nIngrese opción: ").strip()

        if opcion == "1":
            menu_automatizaciones()
        elif opcion == "2":
            menu_gestion_bd()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("[X] Opción inválida.")

def validar_periodo(periodo):
    """Valida el formato del período MM/YYYY."""
    try:
        mes, año = periodo.split('/')
        return len(mes) == 2 and len(año) == 4 and mes.isdigit() and año.isdigit()
    except:
        return False

def validar_fecha(fecha):
    """Valida el formato de fecha DDMMYYYY."""
    return len(fecha) == 8 and fecha.isdigit()

def validar_base_imponible(base):
    """Valida el formato de base imponible (números y punto decimal)."""
    try:
        float(base.replace(',', '.'))
        return True
    except:
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\n[X] Error inesperado: {e}")