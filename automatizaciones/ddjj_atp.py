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

def login_afip(cuit, password, periodo_fiscal, base_imponible, nombre_usuario):
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
        driver.get("https://www.atpformosa.gob.ar/consultas/")
        wait = WebDriverWait(driver, 10)

        # Login ATP
        esperar_y_enviar_texto(driver, wait, By.ID, "cuit", cuit, "CUIT")
        esperar_y_enviar_texto(driver, wait, By.ID, "existing1", password, "contraseña")
        click_elemento(driver, wait, By.NAME, "B1", "botón Ingresar")
        time.sleep(5)

        # Expandir sección "Presentación DDJJ"
        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='#collapseConf']", "botón Presentación DDJJ")
        time.sleep(2)

        # Esperar a que el collapse se expanda completamente
        esperar_elemento(driver, wait, By.ID, "collapseConf", "panel Presentación DDJJ")

        # Scroll al elemento antes de hacer click
        scroll_a_elemento(driver, By.CSS_SELECTOR, "a[href='iibb_ddjj.php']")
        time.sleep(1)

        # Click en "INGRESOS BRUTOS - REGIMEN GENERAL: PRESENTACION DE DDJJ" usando JavaScript
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, "a[href='iibb_ddjj.php']")
            driver.execute_script("arguments[0].click();", elemento)
            print("✔️ Click en INGRESOS BRUTOS - REGIMEN GENERAL")
        except Exception as e:
            print(f"❌ Error al hacer click en INGRESOS BRUTOS: {e}")

        time.sleep(3)

        # Click "Declaración Actividad"
        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='/consultas/iibb_ddjj.php?caseid=actividad_lista']", "Declaración Actividad")
        time.sleep(2)        

        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='iibb_ddjj.php?caseid=actividad_carga']", "Cargar Actividad")
        time.sleep(2)

        # Seleccionar período fiscal
        mes, anio = periodo_fiscal.split('/')

        # Seleccionar mes
        seleccionar_dropdown_por_valor(driver, wait, By.NAME, "n_mes", mes, f"mes {mes}")

        # Seleccionar año
        seleccionar_dropdown_por_valor(driver, wait, By.NAME, "n_anio", anio, f"año {anio}")

        # Click en Aceptar
        click_elemento(driver, wait, By.CSS_SELECTOR, "input[type='submit'][value='Aceptar']", "botón Aceptar período")
        time.sleep(3)

        # Ingresar Base Imponible
        esperar_y_enviar_texto(driver, wait, By.NAME, "base_imponible_0", base_imponible, "Base Imponible")
        time.sleep(1)

        # Click en Aceptar
        click_elemento(driver, wait, By.CSS_SELECTOR, "input[type='submit'][value='Aceptar']", "botón Aceptar Base Imponible")
        time.sleep(3)

        # Verificar mensaje de éxito
        mensaje_exito = esperar_elemento(driver, wait, By.CSS_SELECTOR, "div.alert-verde-20", "mensaje de éxito")
        if mensaje_exito and "LOS DATOS SE CARGARON CORRECTAMENTE" in mensaje_exito.text:
            print("✔️ Datos cargados correctamente")
        else:
            print("⚠️ No se pudo verificar el mensaje de éxito")

        # Click "Deducciones"
        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='/consultas/iibb_ddjj.php?caseid=deducciones_lista']", "Deducciones")
        time.sleep(2)        

        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='iibb_ddjj.php?caseid=deducciones_carga']", "Cargar Deducciones")
        time.sleep(2)

        click_elemento(driver, wait, By.CSS_SELECTOR, "input[type='submit'][value='Aceptar']", "botón Aceptar Deducciones")
        time.sleep(3)

        click_elemento(driver, wait, By.CSS_SELECTOR, "input[type='submit'][value='Guardar']", "botón Guardar Deducciones")
        time.sleep(3)        

        # Click "Liquidación del Impuesto"
        click_elemento(driver, wait, By.CSS_SELECTOR, "a[href='/consultas/iibb_ddjj.php?caseid=ddjj_liquidacion']", "Liquidación del Impuesto")
        time.sleep(2)

        # Scroll y click en "Presentación DJ Mensual" usando JavaScript
        scroll_a_elemento(driver, By.CSS_SELECTOR, "a[href='iibb_ddjj.php?caseid=ddjj_carga']")
        time.sleep(1)

        try:
            elemento = driver.find_element(By.CSS_SELECTOR, "a[href='iibb_ddjj.php?caseid=ddjj_carga']")
            driver.execute_script("arguments[0].click();", elemento)
            print("✔️ Click en Presentación DJ Mensual")
        except Exception as e:
            print(f"❌ Error al hacer click en Presentación DJ Mensual: {e}")

        time.sleep(2)        

        # Mantener navegador abierto para inspección manual
        print("\n⏸️  Navegador abierto para inspección manual")
        print("Presione ENTER para cerrar el navegador y continuar...")
        input()

    except Exception as e:
        driver.save_screenshot(f"atp_login_error_{cuit}.png")
        print(f"Error durante el login: {str(e)}")
    finally:
        driver.quit()
        print("Sesión cerrada.")    