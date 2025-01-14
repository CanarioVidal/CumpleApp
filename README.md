# **CumpleApp**
CumpleApp es una aplicación desarrollada en Python con Flask que permite gestionar cumpleaños y enviar correos automáticos. Es ideal para empresas y marcas que desean personalizar la interacción con sus clientes de manera automatizada.

---

## **Características Principales**
### Gestión de Usuarios (mU)
- Registro de usuarios mediante formularios web.
- Listado y búsqueda de usuarios registrados.
- Seguimiento del estado de redención de regalos.

### Envío de Correos (mC)
- **Automático**:
  - Recordatorios: Enviados 7 días antes del cumpleaños.
  - Saludos de cumpleaños: Enviados el día del cumpleaños.
- **Manual**:
  - Pruebas desde el panel de administración.
  - Configuración de correos personalizados.
  
### Gestión General (mG)
- Tareas programadas utilizando APScheduler.
- Configuración de correo desde `.env`.

---

## **Instalación y Configuración**
1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/CanarioVidal/CumpleApp.git
   cd CumpleApp
