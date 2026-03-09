"""Script de prueba para automatizar carga de retención en Account Soft.

IMPORTANTE:
- Tener Account Soft abierto con la sesión del cliente
- Estar en la pantalla principal de AS-Impuesto
- Ejecutar este script y observar
"""

import time
import pyautogui
import pyperclip
from pywinauto import Desktop
from PIL import ImageGrab
import pytesseract

# Configuración de seguridad
pyautogui.FAILSAFE = True  # Mover mouse a esquina superior izq para detener
pyautogui.PAUSE = 0.5  # Pausa entre acciones

def encontrar_ventana_as():
    """Encuentra y devuelve la ventana de Account Soft."""
    print("[...] Buscando ventana de Account Soft...")
    windows = Desktop(backend="uia").windows()

    for window in windows:
        try:
            title = window.window_text()
            if "AS-Impuesto" in title:
                print(f"[OK] Encontrada: {title}")
                return window
        except:
            pass

    print("[X] No se encontró ventana de Account Soft")
    return None

def abrir_formulario_retenciones():
    """Abre el formulario de retenciones con atajo ALT+V+C+R+R."""
    print("\n[...] Abriendo formulario de retenciones...")
    print("    Presionando: ALT")
    pyautogui.hotkey('alt')
    time.sleep(0.5)

    print("    Presionando: V")
    pyautogui.hotkey('v')
    time.sleep(0.5)

    print("    Presionando: C")
    pyautogui.press('c')
    time.sleep(0.5)

    print("    Presionando: R")
    pyautogui.press('r')
    time.sleep(0.5)

    print("    Presionando: R")
    pyautogui.press('r')
    time.sleep(1)  # Esperar a que abra el formulario

    print("[OK] Formulario debería estar abierto")

def seleccionar_tipo_retencion():
    """Selecciona 'RIVV / Ret. Iva Ventas' en el dropdown Comp."""
    print("\n[...] Seleccionando tipo de retención...")

    # El foco debería estar en el dropdown "Comp."
    print("    Abriendo dropdown (presionando flecha abajo)")
    pyautogui.press('down')
    time.sleep(0.3)

    # Escribir 'RIVV' para buscar en el dropdown
    print("    Escribiendo: RIVV")
    pyautogui.write('RIVV', interval=0.1)
    time.sleep(0.5)

    # Confirmar selección con TAB (va directo al campo Número)
    print("    Confirmando con TAB")
    pyautogui.press('tab')
    time.sleep(0.5)

    print("[OK] Tipo de retención seleccionado")

def ingresar_numero_certificado(numero):
    """Ingresa el número de certificado."""
    print(f"\n[...] Ingresando número de certificado: {numero}")

    # El foco ya está en el campo Número después del TAB anterior
    print(f"    Escribiendo número: {numero}")
    pyautogui.write(str(numero), interval=0.05)
    time.sleep(0.5)

    print(f"[OK] Número {numero} ingresado")

def obtener_razon_seleccionada():
    """Obtiene el texto de la razón social actualmente seleccionada usando pywinauto."""
    try:
        # Buscar específicamente la ventana de Retenciones (no Excel ni otras)
        windows = Desktop(backend="uia").windows()
        ventana_retenciones = None

        for window in windows:
            try:
                title = window.window_text()
                # Buscar ventana que tenga "Retenciones" pero NO "Excel"
                if ("Retenciones" in title or "retenciones" in title) and "Excel" not in title:
                    ventana_retenciones = window
                    break
            except:
                pass

        if not ventana_retenciones:
            return None

        # Buscar el ComboBox de Razón en esa ventana específica
        combos = ventana_retenciones.descendants(control_type="ComboBox")

        for i, combo in enumerate(combos):
            texto = combo.window_text()
            # Saltar el combo de Comp (RIVV)
            if "RIVV" in texto:
                continue
            # Retornar el primer combo que no sea RIVV
            if texto and len(texto) > 1:
                return texto.strip()

    except Exception as e:
        print(f"      [!] Error leyendo control: {e}")
    return None

def seleccionar_razon_social(razon):
    """Selecciona la razón social navegando con flechas y leyendo el control."""
    print(f"\n[...] Seleccionando razón social: {razon}")

    # Pasar al dropdown Razón con TAB
    print("    Navegando al campo Razón (TAB)")
    pyautogui.press('tab')
    time.sleep(0.5)

    # Ir al inicio de la lista con Home (sin abrir dropdown)
    print("    Yendo al inicio (Home)")
    pyautogui.press('home')
    time.sleep(0.5)

    # DEBUG: Probar lectura inicial
    print("    [DEBUG] Probando lectura inicial...")
    test_lectura = obtener_razon_seleccionada()
    if test_lectura:
        print(f"    [DEBUG] ✓ Lectura funciona: {test_lectura}")
    else:
        print("    [DEBUG] ✗ No se pudo leer el control")
        print("    [DEBUG] Intentando método alternativo...")

    # Navegar con flechas y leer el control
    print(f"    Buscando: {razon}")
    razon_upper = razon.upper()
    max_intentos = 150
    encontrado = False

    for i in range(max_intentos):
        # Leer razón actual del control
        texto_actual = obtener_razon_seleccionada()

        if texto_actual:
            texto_upper = texto_actual.upper()

            # Mostrar progreso
            print(f"      [{i+1}] {texto_actual[:50]}")

            # Verificar coincidencia (startswith)
            if texto_upper.startswith(razon_upper):
                print(f"    ✓ Encontrado: {texto_actual}")
                encontrado = True
                break
        else:
            print(f"      [{i+1}] (no se pudo leer)")

        # Siguiente item
        pyautogui.press('down')
        time.sleep(0.15)  # 150ms entre items para dar tiempo a leer

    if encontrado:
        # Confirmar selección con TAB
        print("    Confirmando con TAB")
        pyautogui.press('tab')
        time.sleep(0.5)
        print(f"[OK] Razón social seleccionada")
        return True
    else:
        print(f"[X] No se encontró razón que empiece con: {razon}")
        pyautogui.press('esc')
        time.sleep(0.3)
        return False

def test_carga_retencion():
    """Función principal de prueba."""
    print("="*60)
    print("TEST: Carga de Retención en Account Soft")
    print("="*60)

    # Datos de prueba
    numero_certificado = "12345678"
    razon_social = "BANCO DE FORMOSA"

    print("\n⚠️  PREPARACIÓN:")
    print("1. Tener Account Soft abierto")
    print("2. Estar en la pantalla principal de AS-Impuesto")
    print("3. El script comenzará en 5 segundos...")
    print("4. Si algo sale mal, mueve el mouse a la esquina superior izquierda")

    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    # Encontrar ventana
    ventana_as = encontrar_ventana_as()
    if not ventana_as:
        print("\n[X] ERROR: Account Soft no está abierto")
        return

    # Enfocar ventana
    try:
        ventana_as.set_focus()
        print("[OK] Ventana enfocada")
        time.sleep(0.5)
    except Exception as e:
        print(f"[!] No se pudo enfocar ventana: {e}")
        print("    Continuando de todas formas...")

    # Ejecutar pasos
    try:
        abrir_formulario_retenciones()
        seleccionar_tipo_retencion()
        ingresar_numero_certificado(numero_certificado)
        seleccionar_razon_social(razon_social)

        print("\n" + "="*60)
        print("✓ TEST COMPLETADO")
        print("="*60)
        print(f"Debería verse:")
        print(f"  - Comp: RIVV / Ret. Iva Ventas")
        print(f"  - Número: {numero_certificado}")
        print(f"  - Razón: {razon_social}")
        print("\n¿Los datos se ingresaron correctamente? (S/N)")

    except Exception as e:
        print(f"\n[X] ERROR durante el test: {e}")
        print("    Verifica que Account Soft esté en la pantalla principal")

if __name__ == "__main__":
    test_carga_retencion()
