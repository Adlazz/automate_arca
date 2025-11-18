from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import keyboard
import os
from src.interaccion import esperar_y_enviar_texto, click_elemento, esperar_elemento, scroll_a_elemento
from src.dropdowns import seleccionar_dropdown_por_valor

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def login_afip(cuit, cuit_retenido, password, fecha_desde, fecha_hasta, nombre):
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

        esperar_y_enviar_texto(driver, wait, By.ID, "F1:username", cuit, "CUIT")
        click_elemento(driver, wait, By.ID, "F1:btnSiguiente", "botón Siguiente")
        esperar_y_enviar_texto(driver, wait, By.ID, "F1:password", password, "contraseña")
        click_elemento(driver, wait, By.ID, "F1:btnIngresar", "botón Ingresar")

        time.sleep(5)

        click_elemento(driver, wait, By.LINK_TEXT, "Ver todos", "'Ver todos'")
        retenciones_link = esperar_elemento(driver, wait, By.XPATH, "//h3[contains(text(),'MIS RETENCIONES')]", "MIS RETENCIONES")
        scroll_a_elemento(driver, By.XPATH, "//h3[contains(text(),'MIS RETENCIONES')]")
        driver.execute_script("arguments[0].click();", retenciones_link)

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        print("Cambiado a la nueva pestaña")

        # Esperar a que la nueva página cargue completamente
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)  # Tiempo adicional para elementos dinámicos

        # Buscar el botón "click aquí" por clase (más confiable que ID dinámico)
        print("Buscando botón 'click aquí'...")
        elemento_boton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-tertiary.btn-sm")))
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento_boton)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", elemento_boton)
        print("[OK] Click exitoso en botón 'click aquí'")

        time.sleep(2)

        seleccionar_dropdown_por_valor(driver, wait, By.ID, "cuitRetenido", cuit_retenido, "CUIT Retenido")
        seleccionar_dropdown_por_valor(driver, wait, By.ID, "impuestos", "767", "Impuesto SICORE")

        esperar_y_enviar_texto(driver, wait, By.NAME, "fechaRetencionDesde", fecha_desde, "Fecha Desde")
        esperar_y_enviar_texto(driver, wait, By.NAME, "fechaRetencionHasta", fecha_hasta, "Fecha Hasta")

        click_elemento(driver, wait, By.XPATH, "//input[@type='submit'][@value='Consultar']", "botón Consultar")
        time.sleep(5)

        driver.set_window_size(1170, driver.get_window_size()['height'])
        ruta_base = "D:/Users/Lazzarini1/Desktop/D/ex_mis_docu-D/a_PLANILLAS"
        ruta_destino = os.path.join(ruta_base, nombre, "Retenciones")
        os.makedirs(ruta_destino, exist_ok=True)
        screenshot_path = os.path.join(ruta_destino, f"retenciones_{fecha_desde}_{fecha_hasta}_{cuit_retenido}.png")
        driver.save_screenshot(screenshot_path)
        print(f"[OK] Captura guardada: {screenshot_path}")

        print("Mantén la sesión abierta, presiona 'Esc' para cerrar.")
        while True:
            if keyboard.is_pressed('esc'):
                print("Tecla 'Esc' presionada. Cerrando sesión.")
                break

    except Exception as e:
        driver.save_screenshot(f"afip_login_error_{cuit}.png")
        print(f"[X] Error durante el login: {e}")
    finally:
        driver.quit()
        print("[OK] Sesión cerrada")
