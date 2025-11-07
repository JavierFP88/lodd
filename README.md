# LODD Training Email System

Sistema automatizado de envío de emails para el Multi-Agency Line of Duty Death (LODD) – South Florida Best Practices Training.

## 📋 Descripción

Este sistema permite enviar emails masivos con información de registro para el entrenamiento LODD, dirigido a múltiples agencias de aplicación de la ley y bomberos en el sur de Florida.

## 🚀 Características

- ✅ **Envío masivo de emails** con contenido HTML profesional
- ✅ **Modo de prueba** para validar formato antes del envío masivo
- ✅ **Previsualización de destinatarios** organizados por categorías
- ✅ **Validación automática** de emails y datos
- ✅ **Delay configurable** entre envíos para evitar spam
- ✅ **Reporte detallado** de éxitos y errores
- ✅ **BCC automático** para supervisión

## 📁 Archivos Principales

- `lodd.py` - Script principal del sistema
- `lodd.json` - Base de datos de destinatarios organizados por categorías
- `requirements.txt` - Dependencias de Python

## 📊 Categorías de Destinatarios

### 🎤 **Speakers** (10 destinatarios)
Presentadores y oradores principales del evento

### 👮 **Police Participants** (16+ destinatarios)  
Personal de departamentos de policía participantes

### 🚒 **Fire Participants** (6 destinatarios)
Personal de departamentos de bomberos participantes

## 🛠️ Instalación y Uso

### Prerrequisitos
1. Python 3.x instalado
2. Servicio de email Node.js ejecutándose en puerto 3000
3. Instalar dependencias: `pip install -r requirements.txt`

### Ejecución
```bash
python lodd.py
```

### Opciones del Menú
1. **Previsualizar destinatarios** - Ver todos los destinatarios organizados por categorías
2. **Enviar emails de PRUEBA** - Envío de test a cuentas específicas
3. **Enviar emails masivos** - Envío completo a todos los destinatarios
4. **Salir** - Terminar el programa

## 📧 Contenido del Email

El email incluye:
- **Información del evento** - Detalles del training LODD
- **Enlace de registro** - Link directo para inscripción: https://arcg.is/1P5WOT2
- **Agenda completa** - Cronograma detallado del día
- **Información logística** - Llegada, estacionamiento, almuerzo, dress code
- **Información post-evento** - QR code para survey y certificados

## ⚙️ Configuración

### Variables Principales
```python
SERVICE_URL = "http://10.2.3.133:3000/enviar-correo"
BCC_EMAIL = "cggis@coralgables.com,itsdnotification@coralgables.com"
```

### Estructura del JSON
```json
{
  "Speakers": [...],
  "Participants_Police": [...],
  "Participants_Fire": [...]
}
```

## 🔒 Seguridad

- Validación automática de formatos de email
- Filtrado de destinatarios sin email válido
- BCC para supervisión y auditoria
- Timeout configurado para prevenir colgadas

## 📈 Estadísticas de Uso

- **Total destinatarios**: 32+ personas
- **Emails válidos**: Filtrado automático
- **Delay por defecto**: 2 segundos entre envíos
- **Formato**: HTML responsive

## 👨‍💻 Desarrollado por

**Coral Gables Police Department Training Division**
- Marcos De Rosa - Police Officer
- Sistema desarrollado para entrenamiento Multi-Agency LODD

## 📅 Versión

- **Fecha**: Noviembre 2025
- **Versión**: 1.0
- **Evento**: Multi-Agency Line of Duty Death Training

---

*Este sistema fue desarrollado específicamente para el entrenamiento LODD y está optimizado para el envío masivo de información de registro a múltiples agencias de aplicación de la ley en el sur de Florida.*
