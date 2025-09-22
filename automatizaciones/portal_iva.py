
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

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def login_afip(cuit, password, periodo_fiscal, tipo_operacion, nombre_usuario):
    options = Options()
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
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

