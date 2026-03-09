
"""portal_iva.py - Script principal de automatización para presentar Libro IVA utilizando Selenium."""

import time
import random
import sqlite3
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.interaccion import click_elemento, esperar_elemento, esperar_y_enviar_texto, scroll_a_elemento
from src.dropdowns import click_opcion_dropdown, seleccionar_dropdown_por_valor
from src.uploads import subir_archivos
from src.configuracion_facturacion import seleccionar_modalidad_operacion

def cambiar_representado(driver, wait, cuit_representado):
    """
    Cambia el representado en Portal IVA para personas jurídicas.

    Args:
        driver: WebDriver de Selenium
        wait: WebDriverWait instance
        cuit_representado: CUIT de la persona jurídica a representar

    Returns:
        bool: True si el cambio fue exitoso, False en caso contrario
    """
    try:
        print(f"[INFO] Buscando botón para cambiar representado...")

        # Intentar encontrar el botón/icono de cambiar representado
        # Nota: Los selectores XPath deben ajustarse según la estructura HTML real de Portal IVA
        # Algunas opciones comunes:
        try:
            # Opción 1: Botón con texto específico
            btn_cambiar = esperar_elemento(driver, wait, By.XPATH,
                "//button[contains(text(), 'Cambiar')] | //a[contains(text(), 'Cambiar')]",
                "botón cambiar representado", timeout=5)
        except:
            # Opción 2: Icono cerca del encabezado "REPRESENTANDO A:"
            btn_cambiar = esperar_elemento(driver, wait, By.XPATH,
                "//div[contains(text(), 'REPRESENTANDO A:')]/following-sibling::*//button | //div[contains(text(), 'REPRESENTANDO A:')]/following-sibling::*//a",
                "icono cambiar representado", timeout=5)

        btn_cambiar.click()
        print("[OK] Click en botón cambiar representado")
        time.sleep(2)

        # Esperar que aparezca el modal o dropdown de selección
        # Intentar buscar campo de búsqueda o lista de CUITs
        try:
            # Opción 1: Campo de búsqueda/input para CUIT
            campo_cuit = esperar_elemento(driver, wait, By.XPATH,
                "//input[@type='text'] | //input[@placeholder]",
                "campo CUIT representado", timeout=5)
            campo_cuit.clear()
            campo_cuit.send_keys(cuit_representado)
            time.sleep(1)

            # Buscar en lista de resultados
            opcion_cuit = esperar_elemento(driver, wait, By.XPATH,
                f"//li[contains(text(), '{cuit_representado}')] | //div[contains(text(), '{cuit_representado}')]",
                "opción CUIT en lista")
            opcion_cuit.click()

        except:
            # Opción 2: Dropdown/select directo
            print("[INFO] Intentando seleccionar desde dropdown...")
            seleccionar_dropdown_por_valor(driver, wait, By.XPATH,
                "//select", cuit_representado, "representado")

        # Buscar botón de confirmar/aceptar
        try:
            btn_confirmar = esperar_elemento(driver, wait, By.XPATH,
                "//button[contains(text(), 'Aceptar')] | //button[contains(text(), 'Confirmar')] | //button[contains(text(), 'OK')]",
                "botón confirmar", timeout=5)
            btn_confirmar.click()
        except:
            print("[INFO] No se encontró botón de confirmación (podría ser automático)")

        time.sleep(3)

        # Verificar que el cambio fue exitoso
        try:
            header = driver.find_element(By.XPATH, "//div[contains(text(), 'REPRESENTANDO A:')]").text
            if cuit_representado in header:
                print(f"[OK] Representado cambiado exitosamente a CUIT: {cuit_representado}")
                return True
            else:
                print(f"[X] El CUIT {cuit_representado} no aparece en el header")
                return False
        except:
            print("[!] No se pudo verificar el cambio de representado")
            return True  # Asumir éxito si no hay error anterior

    except Exception as e:
        print(f"[X] Error al cambiar representado: {str(e)}")
        print("[!] Continuando con el CUIT por defecto...")
        return False

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def login_afip(cuit, password, periodo_fiscal, tipo_operacion, nombre_usuario, cuit_representado=None):
    options = Options()
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")
        wait = WebDriverWait(driver, 10)

        # Log In ARCA
        esperar_y_enviar_texto(driver, wait, By.ID, "F1:username", cuit, "CUIT")
        click_elemento(driver, wait, By.ID, "F1:btnSiguiente", "botón Siguiente")
        esperar_y_enviar_texto(driver, wait, By.ID, "F1:password", password, "contraseña")
        click_elemento(driver, wait, By.ID, "F1:btnIngresar", "botón Ingresar")
        time.sleep(5)

        click_elemento(driver, wait, By.LINK_TEXT, "Ver todos", "'Ver todos'")
        portal_iva_link = esperar_elemento(driver, wait, By.XPATH, "//h3[contains(text(),'PORTAL IVA')]", "PORTAL IVA")
        scroll_a_elemento(driver, By.XPATH, "//h3[contains(text(),'PORTAL IVA')]")
        driver.execute_script("arguments[0].click();", portal_iva_link)
        time.sleep(5)

        # Cambio de pestaña
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        print("Cambiado a la nueva pestaña")

        click_elemento(driver, wait, By.XPATH, "//button[span[text()='Ingresar']]", "botón Ingresar")
        periodo_valor = periodo_fiscal[3:] + periodo_fiscal[:2]
        seleccionar_dropdown_por_valor(driver, wait, By.ID, "periodo", periodo_valor, "período fiscal")

        click_elemento(driver, wait, By.XPATH, "//button[span[text()='Continuar']]", "botón Continuar")

        # 🆕 NUEVA LÓGICA: Cambiar representado si es Persona Jurídica
        if cuit_representado:
            print(f"[INFO] Persona Jurídica detectada. Cambiando a representado CUIT: {cuit_representado}")
            cambiar_representado(driver, wait, cuit_representado)
        else:
            print(f"[INFO] Persona Física. Usando CUIT por defecto: {cuit}")

        click_elemento(driver, wait, By.XPATH, "//button[span[text()='Ingresar']]", "botón Ingresar (2)")

        esperar_elemento(driver, wait, By.ID, "seccionConMovimientos", "sección checkboxes")
        seleccionar_modalidad_operacion(driver, wait, tipo_operacion)

        click_elemento(driver, wait, By.ID, "btnGuardar", "botón Guardar")
        click_elemento(driver, wait, By.XPATH, "//h3[contains(text(), 'Libro Ventas')]", "sección Libro Ventas")

        click_opcion_dropdown(driver, wait, "btnDropdownImportar", "lnkImportarArchivo")
        subir_archivos(driver, wait, nombre_usuario, periodo_valor, tipo="ventas")

        click_elemento(driver, wait, By.XPATH, "//a[contains(@class, 'btn-success') and contains(text(), 'Continuar al Libro Compras')]", "botón Continuar al Libro Compras")
        click_opcion_dropdown(driver, wait, "btnDropdownImportar", "lnkImportarArchivo")
        subir_archivos(driver, wait, nombre_usuario, periodo_valor, tipo="compras")

        click_elemento(driver, wait, By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Volver al Libro')]", "botón Volver al Libro")

        print("Mantén la sesión abierta, presiona 'Esc' para cerrar.")
        while True:
            if keyboard.is_pressed('esc'):
                print("Tecla 'Esc' presionada. Cerrando sesión.")
                break

    except Exception as e:
        driver.save_screenshot(f"afip_login_error_{cuit}.png")
        print(f"Error durante el login: {str(e)}")
    finally:
        driver.quit()
        print("Sesión cerrada.")

