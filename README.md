# Automate ARCA

Sistema de automatización para procesos de AFIP/ARCA usando Python y Selenium.

## Descripción

Este proyecto automatiza dos procesos principales de AFIP:
- **Presentación de Libro IVA**: Automatiza la presentación del Libro IVA en el Portal IVA
- **Consulta de Retenciones**: Automatiza la consulta de retenciones realizadas

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

Ejecuta el programa principal:

```bash
python main.py
```

### Opciones disponibles:

1. **Presentar Libro IVA**
   - Formato de período: MM/YYYY (ej: 03/2024)
   - Tipos de operación: N (Ninguna) o E (Exentas)

2. **Consultar Retenciones**
   - Formato de fechas: DDMMYYYY (ej: 01032024)

## Estructura del Proyecto

```
automate_arca/
├── main.py                 # Menú principal
├── automatizaciones/       # Módulos de automatización
├── database/              # Base de datos y DAOs
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Tecnologías Utilizadas

- **Python**: Lenguaje principal
- **Selenium**: Automatización web
- **SQLite**: Base de datos
- **Requests**: Peticiones HTTP

## Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de uso interno.