
"""dropdowns.py - Funciones para interactuar con menús desplegables."""

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def click_opcion_dropdown(driver, wait, id_boton, id_opcion):
    from src.interaccion import click_elemento
    click_elemento(driver, wait, By.ID, id_boton, "botón dropdown")
    click_elemento(driver, wait, By.ID, id_opcion, "opción del menú")

def seleccionar_dropdown_por_valor(driver, wait, by, selector, valor, descripcion="dropdown"):
    try:
        dropdown = wait.until(EC.presence_of_element_located((by, selector)))
        Select(dropdown).select_by_value(valor)
        print(f"✔️ Opción '{valor}' seleccionada en {descripcion}")
    except Exception as e:
        print(f"❌ No se pudo seleccionar '{valor}' en {descripcion}: {e}")
        driver.save_screenshot(f"error_dropdown_{descripcion}.png")
