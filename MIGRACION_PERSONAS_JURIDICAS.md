# Migración Base de Datos - Soporte Personas Jurídicas

## 📋 Resumen de Cambios

Esta refactorización reorganiza la base de datos para manejar correctamente personas jurídicas (PJ) con sus representantes legales.

### Modelo Anterior (Inconsistente)
```
usuarios
├── nombre: nombre del usuario (confuso: ¿PF o PJ?)
├── cuit: CUIT usado para login
├── cuit_retenido: CUIT del contribuyente
├── password
└── password_atp
```

### Modelo Nuevo (Clarificado)
```
usuarios
├── nombre: Nombre del CONTRIBUYENTE (PJ o PF)
├── cuit: CUIT del CONTRIBUYENTE (quien presenta DDJJ)
├── cuit_representante: CUIT para login ARCA (NULL si es PF)
├── nombre_representante: Nombre representante legal (NULL si es PF)
├── password: Password ARCA
└── password_atp: Password ATP
```

## 🔄 Proceso de Migración

### Paso 1: Backup Actual
Antes de migrar, el script creará automáticamente un backup:
```
database/usuarios.db.backup_YYYYMMDD_HHMMSS
```

### Paso 2: Ejecutar Migración
```bash
python scripts/migrar_db_personas_juridicas.py
```

El script:
1. Crea backup automático
2. Crea nueva tabla con estructura actualizada
3. Migra datos existentes con conversión lógica
4. Elimina tabla antigua
5. Renombra tabla nueva
6. Muestra resumen de datos migrados

### Paso 3: Ajustes Manuales Post-Migración

⚠️ **IMPORTANTE**: Después de la migración, revisar y corregir:

1. **Nombres de Representantes**: El script genera nombres genéricos como "REPRESENTANTE DE [NOMBRE]"
2. **Nombres de Contribuyentes**: Asegurar que el nombre corresponda a la PJ, no a la PF

#### Ejemplo de Ajustes Necesarios

**Antes de ajustar:**
```
Nombre: GIMENEZ KARINA NATALIA
CUIT: 33-11111111-9 (condominio)
CUIT Representante: 27-22222222-3
Nombre Representante: REPRESENTANTE DE GIMENEZ KARINA NATALIA
```

**Después de ajustar:**
```
Nombre: CONDOMINIO GIMENEZ KARINA NATALIA
CUIT: 33-11111111-9
CUIT Representante: 27-22222222-3
Nombre Representante: GIMENEZ KARINA NATALIA
```

Usar el menú de gestión de BD (opción 3 - Modificar Usuario) para realizar ajustes.

## 📝 Ejemplos de Datos Correctos

### Persona Jurídica - SRL
```
Nombre: LAZZARINI & LAZZARINI SRL
CUIT: 30-12345678-9
CUIT Representante: 20-98765432-1
Nombre Representante: LAZZARINI JULIO OMAR
Password: ****
Password ATP: ****
```

### Persona Jurídica - Condominio
```
Nombre: CONDOMINIO GIMENEZ KARINA NATALIA
CUIT: 33-11111111-9
CUIT Representante: 27-22222222-3
Nombre Representante: GIMENEZ KARINA NATALIA
Password: ****
Password ATP: ****
```

### Persona Física
```
Nombre: FERNANDEZ JOSE LUIS
CUIT: 20-33333333-5
CUIT Representante: NULL
Nombre Representante: NULL
Password: ****
Password ATP: ****
```

## 🆕 Nuevas Funcionalidades

### Insertar Nuevo Usuario
El menú ahora pregunta el tipo de persona:

**[J] Persona Jurídica:**
- Solicita nombre de la PJ (ej: "LAZZARINI & LAZZARINI SRL")
- Solicita CUIT de la PJ
- Solicita nombre del representante legal
- Solicita CUIT del representante (para login)

**[F] Persona Física:**
- Solicita nombre de la PF
- Solicita CUIT (mismo para login y presentación)

### Portal IVA - Cambio de Representado
Nueva función `cambiar_representado()` en `portal_iva.py`:
- Detecta automáticamente si es PJ (tiene `cuit_representante`)
- Busca el botón/icono de cambiar representado
- Selecciona el CUIT de la persona jurídica
- Verifica el cambio exitoso

⚠️ **Nota**: Los selectores XPath pueden requerir ajustes según la estructura HTML real de Portal IVA de ARCA.

## 🔍 Lógica de Uso

### Portal IVA
```python
# Si tiene representante, usa el CUIT del representante para login
cuit_login = cuit_representante if cuit_representante else cuit

# Si tiene representante, el CUIT del contribuyente es el representado
cuit_representado = cuit if cuit_representante else None
```

### Consultar Retenciones
```python
# Login con CUIT del representante (o propio si es PF)
cuit_login = cuit_representante if cuit_representante else cuit

# Consultar siempre por el CUIT del contribuyente principal
cuit_retenido = cuit
```

## 🧪 Testing

Después de la migración, probar:

1. **Listar usuarios** (Menú 2 → Opción 2)
   - Verificar que se muestren correctamente PF y PJ
   - Revisar que los representantes aparezcan solo en PJ

2. **Insertar nueva PJ** (Menú 2 → Opción 1 → J)
   - Probar flujo completo de inserción

3. **Insertar nueva PF** (Menú 2 → Opción 1 → F)
   - Probar flujo completo de inserción

4. **Portal IVA con PJ**
   - Seleccionar una PJ
   - Verificar que intente cambiar el representado
   - Observar logs para detectar problemas

5. **Consultar Retenciones**
   - Probar con PF y PJ
   - Verificar que use los CUITs correctos

## 🐛 Troubleshooting

### Error: "Ya existe un usuario con ese CUIT"
- El nuevo modelo usa `cuit` (del contribuyente) como UNIQUE
- Verificar que no existan duplicados del CUIT del contribuyente

### Portal IVA no cambia representado
- Los selectores XPath en `cambiar_representado()` pueden necesitar ajuste
- Usar herramientas de desarrollo del navegador para identificar elementos correctos
- Revisar logs de ejecución para ver dónde falla

### Credenciales incorrectas
- Verificar que `cuit_representante` tenga las credenciales correctas
- Para PF, asegurar que `cuit_representante` sea NULL

## 📞 Restaurar desde Backup

Si algo sale mal:
```python
import shutil
shutil.copy('database/usuarios.db.backup_YYYYMMDD_HHMMSS', 'database/usuarios.db')
```

## ✅ Checklist Post-Migración

- [ ] Ejecutar script de migración
- [ ] Revisar datos migrados con "Consultar usuarios"
- [ ] Ajustar nombres de contribuyentes (PJ vs PF)
- [ ] Ajustar nombres de representantes
- [ ] Probar inserción de nueva PJ
- [ ] Probar inserción de nueva PF
- [ ] Probar Portal IVA con PJ
- [ ] Probar Portal IVA con PF
- [ ] Probar Consultar Retenciones
- [ ] Ajustar selectores XPath si es necesario
