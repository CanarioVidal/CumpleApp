CumpleApp - Documentación del Proyecto
Descripción General
CumpleApp es una aplicación desarrollada en Python con Flask y SQLite. Su propósito es gestionar registros de usuarios con fechas de cumpleaños y enviar correos electrónicos con obsequios en dos momentos clave:

15 días antes del cumpleaños.
El mismo día del cumpleaños.
Características Principales
Registro de Cumpleaños:

Formulario con validación para aceptar solo usuarios mayores de 18 años.
Integración AJAX para envíos sin recargar la página.
Panel de Administración:

Gestión de cumpleaños del día.
Consulta dinámica de usuarios.
Registro de redención del obsequio mediante checkboxes.
Eliminación de registros (individual o múltiple).
Diseño moderno con Bootstrap.
Seguridad:

Sistema básico de autenticación para el acceso al panel de administración.
Requisitos del Sistema
Python 3.10 o superior.
Bibliotecas necesarias:
bash
Copiar código
pip install flask flask_sqlalchemy python-dotenv
Base de Datos: SQLite.
Instalación y Configuración
Clonar el repositorio:

bash
Copiar código
git clone https://github.com/CanarioVidal/CumpleApp.git
cd CumpleApp
Crear entorno virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\\venv\\Scripts\\activate  # Windows
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurar el entorno:

bash
Copiar código
python run.py
Abrir la aplicación en el navegador:

arduino
Copiar código
http://127.0.0.1:5000
Uso de la Aplicación
1. Registro de Usuarios:
Página dedicada para agregar cumpleaños:
arduino
Copiar código
http://127.0.0.1:5000/agregar-cumple
Validación en el formulario para aceptar solo mayores de 18 años.
2. Panel de Administración:
URL protegida por autenticación:
arduino
Copiar código
http://127.0.0.1:5000/admin
Funciones:
Visualizar cumpleaños del día.
Actualizar estado de redención.
Buscar usuarios dinámicamente.
Agregar nuevos registros.
Módulos Importantes
Rutas (routes.py):

Maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
Incluye autenticación y AJAX para mejorar la experiencia de usuario.
Modelos (models.py):

Define la estructura de la base de datos con SQLAlchemy.
Configuración (settings.py):

Permite personalizar parámetros como la clave secreta y la URI de la base de datos.
Plantillas HTML:

Construidas con Bootstrap para diseño responsivo.
Preparadas para futuras mejoras como tema oscuro.
Próximas Funcionalidades
Envío de Correos Electrónicos:

Automatizar el envío de correos electrónicos con mensajes personalizados.
Programar notificaciones para enviar 15 días antes y el mismo día del cumpleaños.
Soporte para Tema Oscuro:

Mejorar la experiencia visual según la configuración del dispositivo.
Escalabilidad:

Adaptar la base de datos para utilizar PostgreSQL o MySQL en producción.

Notas Finales
Este proyecto está diseñado para ser escalable. Aunque actualmente está orientado a cumplir con funcionalidades básicas de registro y gestión, futuras versiones podrán incorporar herramientas avanzadas para automatización de campañas por correo y configuraciones personalizadas.

