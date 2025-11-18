
"""interaccion.py - Funciones reutilizables de interacción con elementos en Selenium."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_elemento(driver, wait, by, selector, descripcion="elemento", screenshot_name=None):
    try:
        elemento = wait.until(EC.element_to_be_clickable((by, selector)))
        elemento.click()
        print(f"[OK] Click en {descripcion}")
    except Exception as e:
        print(f"[X] Error al hacer clic en {descripcion}: {e}")
        if screenshot_name:
            driver.save_screenshot(screenshot_name)

def esperar_elemento(driver, wait, by, selector, descripcion="elemento"):
    try:
        elemento = wait.until(EC.presence_of_element_located((by, selector)))
        print(f"[OK] {descripcion} presente")
        return elemento
    except Exception as e:
        print(f"[X] No se encontró {descripcion}: {e}")
        return None

def esperar_y_enviar_texto(driver, wait, by, selector, texto, descripcion="input"):
    try:
        input_field = wait.until(EC.presence_of_element_located((by, selector)))
        input_field.clear()
        input_field.send_keys(texto)
        print(f"[OK] Texto ingresado en {descripcion}")
    except Exception as e:
        print(f"[X] No se pudo ingresar texto en {descripcion}: {e}")

def scroll_a_elemento(driver, by, selector):
    try:
        elemento = driver.find_element(by, selector)
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(0.5)
        print("[OK] Scrolled hacia el elemento")
    except Exception as e:
        print(f"[X] Error al scrollear hacia el elemento: {e}")
