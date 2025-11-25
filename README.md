# Automate ARCA

Sistema de automatización para procesos de AFIP/ARCA usando Python y Selenium.

## Descripción

Este proyecto automatiza tres procesos principales de AFIP/ARCA:
- **Presentación de Libro IVA**: Automatiza la presentación del Libro IVA en el Portal IVA
- **Consulta de Retenciones**: Automatiza la consulta de retenciones realizadas
- **DDJJ ATP (Rentas Formosa)**: Automatiza la presentación de DDJJ de Ingresos Brutos

## Características

- Interfaz de línea de comandos intuitiva
- Gestión de múltiples usuarios y CUITs
- Base de datos SQLite para almacenar usuarios
- Automatización web con Selenium
- Validación de formatos de fechas y períodos

## Requisitos

- Python 3.x
- Las dependencias listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd automate_arca
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Opción 1: Ejecutar como ejecutable (.exe)

La forma más sencilla de usar el programa es a través del ejecutable pre-compilado:

1. Descarga `auto_arca.exe` de la carpeta `dist/`
2. Ejecuta el archivo:
   - Doble clic en `auto_arca.exe` o
   - Desde la terminal: `auto_arca.exe`

### Opción 2: Ejecutar desde Python

```bash
python main.py
```

### Opciones disponibles:

1. **Consultar Retenciones**
   - Formato de fechas: DDMMYYYY (ej: 01032024)

2. **Presentar Libro IVA**
   - Formato de período: MM/YYYY (ej: 03/2024)
   - Tipos de operación: N (Ninguna) o E (Exentas)

3. **Presentar DDJJ ATP**
   - Formato de período: MM/YYYY (ej: 03/2024)
   - Base Imponible: usar punto como separador decimal (ej: 999.99)

## Compilar el ejecutable

Si necesitas generar el .exe desde el código fuente:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "database;database" --add-data "automatizaciones;automatizaciones" --add-data "scripts;scripts" --hidden-import=selenium --hidden-import=webdriver_manager main.py
```

El ejecutable se generará en la carpeta `dist/`.

## Estructura del Proyecto

```
automate_arca/
├── main.py                 # Menú principal
├── automatizaciones/       # Módulos de automatización
│   ├── portal_iva.py      # Automatización Portal IVA
│   ├── consultar_retenciones.py  # Consulta de retenciones
│   └── ddjj_atp.py        # DDJJ ATP Formosa
├── database/              # Base de datos y DAOs
│   ├── usuarios.db        # Base de datos SQLite
│   └── dao/               # Data Access Objects
├── src/                   # Utilidades de Selenium
├── scripts/               # Scripts auxiliares
├── requirements.txt       # Dependencias
├── dist/                  # Ejecutable compilado
└── README.md             # Este archivo
```

## Tecnologías Utilizadas

- **Python**: Lenguaje principal
- **Selenium**: Automatización web
- **SQLite**: Base de datos
- **PyInstaller**: Generación de ejecutables
- **ChromeDriver**: Driver para automatización con Chrome

## Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de uso interno.