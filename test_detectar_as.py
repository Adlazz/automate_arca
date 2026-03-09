"""Script de prueba para detectar ventana de Account Soft."""

from pywinauto import Desktop
import time

print("Buscando ventanas de Account Soft...")
print("\nVentanas abiertas:\n")

windows = Desktop(backend="uia").windows()

for i, window in enumerate(windows):
    try:
        title = window.window_text()
        if title:  # Solo mostrar ventanas con título
            print(f"{i+1}. {title}")

            # Buscar específicamente Account Soft
            if "AS-Impuesto" in title or "Account Soft" in title or "Lazzarini" in title:
                print(f"   ⭐ ENCONTRADA: Account Soft")
                print(f"   Class: {window.class_name()}")
    except Exception as e:
        pass

print("\n" + "="*60)
print("Presiona Ctrl+C para salir")
