# Instrucciones para Reconstruir el Ejecutable

## Requisitos Previos

- Python 3.x instalado
- PyInstaller instalado (`pip install pyinstaller`)
- Todas las dependencias del proyecto instaladas

## Instalación de Dependencias

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Construcción del Ejecutable

### Opción 1: Usar el archivo .spec existente (recomendado)

```bash
pyinstaller auto_arca.spec
```

### Opción 2: Generar desde cero

```bash
pyinstaller --onefile --console --name auto_arca --add-data "database/usuarios.db;database" main.py
```

**Nota para Windows:** Si usas Git Bash o MSYS2, cambia el separador `;` por `:` en `--add-data`:
```bash
pyinstaller --onefile --console --name auto_arca --add-data "database/usuarios.db:database" main.py
```

## Ubicación del Ejecutable

El archivo ejecutable se generará en:
```
dist/auto_arca.exe
```

## Limpieza (Opcional)

Para limpiar archivos temporales generados durante la compilación:

```bash
rm -rf build dist __pycache__
```

## Notas Importantes

1. El archivo `auto_arca.spec` incluye la base de datos `database/usuarios.db` en el ejecutable
2. El ejecutable es standalone y no requiere Python instalado para ejecutarse
3. Si se modifica la estructura de archivos o dependencias, regenerar el .spec con PyInstaller
4. El ejecutable se compila con UPX compression habilitado para reducir tamaño

## Troubleshooting

- Si faltan módulos al ejecutar: agregar a `hiddenimports=[]` en `auto_arca.spec`
- Si falta la base de datos: verificar que `database/usuarios.db` exista antes de compilar
- Si el ejecutable es muy grande: verificar que UPX esté instalado (`upx=True` en .spec)
