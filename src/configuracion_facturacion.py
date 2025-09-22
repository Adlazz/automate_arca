
"""configuracion_facturacion.py - Configura si el usuario tiene operaciones exentas o ninguna."""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def seleccionar_modalidad_operacion(driver, wait, tipo):
    from src.interaccion import scroll_a_elemento
    try:
        if tipo == "ninguna":
            label_xpath = "//label[contains(text(), 'No realizo ninguna actividad anterior')]"
            label = wait.until(EC.element_to_be_clickable((By.XPATH, label_xpath)))
            scroll_a_elemento(driver, By.XPATH, label_xpath)
            driver.execute_script("arguments[0].click();", label)
            print("✔️ 'No realizo ninguna actividad anterior' marcado")

        elif tipo == "exentas":
            label_xpath = "//label[contains(text(), 'Operaciones No Gravadas o Exentas')]"
            label = wait.until(EC.element_to_be_clickable((By.XPATH, label_xpath)))
            scroll_a_elemento(driver, By.XPATH, label_xpath)
            driver.execute_script("arguments[0].click();", label)
            print("✔️ 'Operaciones No Gravadas o Exentas' marcado")

            for _ in range(10):
                dropdown = driver.find_element(By.ID, "tipoProrrateo")
                if dropdown.is_enabled():
                    break
                time.sleep(0.5)
            else:
                print("❌ Dropdown no habilitado")
                driver.save_screenshot("error_dropdown_disabled.png")
                return

            boton_xpath = "//div[@class='btn-group bootstrap-select form-control']//button"
            boton_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, boton_xpath)))
            scroll_a_elemento(driver, By.XPATH, boton_xpath)
            driver.execute_script("arguments[0].click();", boton_dropdown)
            print("✔️ Click en el botón del dropdown")

            opciones = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//ul[@class='dropdown-menu inner']/li/a/span[@class='text']"
            )))
            for opcion in opciones:
                if opcion.text.strip() == "Con prorrateo global":
                    driver.execute_script("arguments[0].click();", opcion)
                    print("✔️ Opción 'Con prorrateo global' seleccionada")
                    break
            else:
                print("❌ No se encontró la opción 'Con prorrateo global'")

        else:
            print("❌ Tipo de operación inválido. Usá 'ninguna' o 'exentas'.")

    except Exception as e:
        print("⚠️ Excepción al seleccionar la modalidad de operación")
        print(f"Detalle: {e}")
        driver.save_screenshot("error_modalidad_operacion.png")
