
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

def cambiar_representado(driver, wait, nombre_contribuyente, cuit_representado):
    """
    Cambia el representado en Portal IVA para personas jurídicas.

    Args:
        driver: WebDriver de Selenium
        wait: WebDriverWait instance
        nombre_contribuyente: Nombre del contribuyente (PJ) a representar
        cuit_representado: CUIT de la persona jurídica a representar (formato: 30711019509)

    Returns:
        bool: True si el cambio fue exitoso, False en caso contrario
    """
    try:
        print(f"[INFO] Cambiando a representado: {nombre_contribuyente}", flush=True)

        # Paso 1: Click en el icono de cambio de relación
        # Elemento: <a title="cambio relación" href="#/changeRelation">
        click_elemento(driver, wait, By.XPATH,
            "//a[@title='cambio relación'][@href='#/changeRelation']",
            "icono cambio relación")

        time.sleep(3)

        # Guardar screenshot y HTML para debug
        driver.save_screenshot("debug_cambio_relacion.png")
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[DEBUG] Screenshot y HTML guardados", flush=True)

        # Paso 2: Click en el elemento del representado
        # Intentar múltiples estrategias de búsqueda

        # Formatear CUIT con guiones
        cuit_formateado = f"{cuit_representado[:2]}-{cuit_representado[2:10]}-{cuit_representado[10]}"
        print(f"[INFO] Buscando representado: {nombre_contribuyente} (CUIT: {cuit_formateado})", flush=True)

        # Estrategia 1: Buscar por nombre en h3
        try:
            print("[DEBUG] Intentando estrategia 1: nombre en h3", flush=True)
            xpath_1 = f"//a[@class='panel panel-default'][@title='Representar a...']//h3[contains(text(), '{nombre_contribuyente}')]"
            elemento = driver.find_element(By.XPATH, xpath_1)
            elemento.click()
            print(f"[OK] Click exitoso usando nombre en h3", flush=True)
            time.sleep(2)
            return True
        except Exception as e1:
            print(f"[INFO] Estrategia 1 falló: {str(e1)}", flush=True)

        # Estrategia 2: Buscar por CUIT formateado en small
        try:
            xpath_2 = f"//a[@class='panel panel-default'][@title='Representar a...']//small[contains(text(), 'CUIT {cuit_formateado}')]"
            elemento = driver.find_element(By.XPATH, xpath_2)
            # Click en el elemento padre (el <a>)
            elemento.find_element(By.XPATH, "./ancestor::a[@class='panel panel-default']").click()
            print(f"[OK] Click exitoso usando CUIT en small")
            time.sleep(2)
            return True
        except Exception as e2:
            print(f"[INFO] Estrategia 2 falló: {str(e2)}")

        # Estrategia 3: Buscar el div.media que contiene el nombre
        try:
            xpath_3 = f"//div[@class='media']//h3[contains(text(), '{nombre_contribuyente}')]"
            elemento = driver.find_element(By.XPATH, xpath_3)
            # Click en el elemento padre <a>
            elemento.find_element(By.XPATH, "./ancestor::a[@class='panel panel-default']").click()
            print(f"[OK] Click exitoso usando div.media")
            time.sleep(2)
            return True
        except Exception as e3:
            print(f"[INFO] Estrategia 3 falló: {str(e3)}")

        # Estrategia 4: Buscar cualquier h3 que contenga parte del nombre
        try:
            # Usar las primeras palabras del nombre
            palabras = nombre_contribuyente.split()[:3]  # Primeras 3 palabras
            nombre_parcial = " ".join(palabras)
            xpath_4 = f"//h3[contains(text(), '{nombre_parcial}')]"
            elemento = driver.find_element(By.XPATH, xpath_4)
            # Click en el elemento padre <a>
            elemento.find_element(By.XPATH, "./ancestor::a[@class='panel panel-default']").click()
            print(f"[OK] Click exitoso usando nombre parcial")
            time.sleep(2)
            return True
        except Exception as e4:
            print(f"[INFO] Estrategia 4 falló: {str(e4)}")

        # Estrategia 5: Click directo en cualquier panel con title="Representar a..."
        try:
            xpath_5 = "//a[@class='panel panel-default'][@title='Representar a...']"
            elementos = driver.find_elements(By.XPATH, xpath_5)
            print(f"[INFO] Encontrados {len(elementos)} elementos 'Representar a...'")

            # Buscar el que contenga el nombre o CUIT
            for idx, elem in enumerate(elementos):
                texto = elem.text.upper()
                print(f"[INFO] Elemento {idx+1}: {texto[:100]}...")
                if nombre_contribuyente.upper() in texto or cuit_formateado in texto:
                    elem.click()
                    print(f"[OK] Click exitoso en elemento {idx+1}")
                    time.sleep(2)
                    return True
        except Exception as e5:
            print(f"[INFO] Estrategia 5 falló: {str(e5)}")

        print("[X] Todas las estrategias fallaron")
        return False

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

        # 🆕 NUEVA LÓGICA: Cambiar representado si es Persona Jurídica
        # IMPORTANTE: Esto debe hacerse ANTES de hacer click en "Ingresar"
        if cuit_representado:
            print(f"[INFO] Persona Jurídica detectada. Cambiando a representado: {nombre_usuario}", flush=True)
            cambiar_representado(driver, wait, nombre_usuario, cuit_representado)
        else:
            print(f"[INFO] Persona Física. Usando CUIT por defecto: {cuit}", flush=True)

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

