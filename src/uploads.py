
"""uploads.py - Funciones para subir archivos de ventas o compras en AFIP."""

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def subir_archivos(driver, wait, nombre, periodo_valor, tipo="ventas"):
    base_path = os.path.join(r'C:\Users\usuario\Documents\Adrian\CyV', nombre)
    archivo_path = os.path.join(base_path, f'{tipo}_{periodo_valor}.txt')
    alicuotas_path = os.path.join(base_path, f'{tipo}_{periodo_valor}_alicuotas.txt')

    try:
        input_archivo = wait.until(EC.presence_of_element_located((By.ID, 'archivo')))
        input_archivo.send_keys(archivo_path)
        print(f"[OK] Archivo {tipo} subido: {archivo_path}")
    except Exception as e:
        print(f"[X] Error al subir archivo {tipo}: {e}")
        driver.save_screenshot(f"error_{tipo}.png")
        raise

    try:
        input_alicuotas = wait.until(EC.presence_of_element_located((By.ID, 'archivoIVA')))
        input_alicuotas.send_keys(alicuotas_path)
        print(f"[OK] Archivo de alícuotas subido: {alicuotas_path}")
    except Exception as e:
        print(f"[X] Error al subir alícuotas de {tipo}: {e}")
        driver.save_screenshot(f"error_alicuotas_{tipo}.png")
        raise

    try:
        importar_btn = wait.until(EC.element_to_be_clickable((By.ID, 'btnImportarArchivosImportar')))
        importar_btn.click()
        print("[OK] Clic en botón Importar")
    except Exception as e:
        print(f"[X] Error al hacer clic en Importar: {e}")
        driver.save_screenshot(f"error_importar_{tipo}.png")
        raise

    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fa-circle-o-notch.fa-spin")))
        print("[OK] Importación completada")
        time.sleep(4)
    except Exception as e:
        print(f"[!] No se pudo confirmar finalización de importación: {e}")

    try:
        contenedor = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "btnTareasCerrar"))
        )
        cerrar_btn = contenedor.find_element(By.XPATH, ".//button[contains(text(), 'Cerrar')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", cerrar_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", cerrar_btn)
        print("[OK] Clic en botón Cerrar del modal")
    except Exception as e:
        print(f"[!] No se pudo hacer clic en el botón Cerrar: {e}")
        driver.save_screenshot(f"error_cerrar_modal_{tipo}.png")
