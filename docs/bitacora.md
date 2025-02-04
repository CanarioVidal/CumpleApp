**Bitácora del Proyecto CumpleApp**

---

### **Etapa 1: Inicio del Proyecto**

#### **Objetivo Principal**
Automatizar el envío de correos de felicitación y recordatorios de cumpleaños basado en intervalos de fechas y el día exacto del cumpleaños.

#### **Decisiones Iniciales**
1. **Herramientas y Tecnologías**:
   - Lenguaje de programación: Python.
   - Framework: Flask.
   - Base de datos: SQLite.
   - Envio de emails: Flask-Mail.
   - Tareas programadas: APScheduler.

2. **Requisitos del Sistema**:
   - Registro de usuarios con nombre, correo y fecha de cumpleaños.
   - Envío automático de correos.
   - Interfaz administrativa para consultar y gestionar usuarios.

3. **Estructura Inicial del Proyecto**:
   - Archivos principales:
     - **app.py**: Configuración del servidor.
     - **routes.py**: Manejo de rutas.
     - **models.py**: Definición de la base de datos.
     - **tasks.py**: Automatización de envío de correos.

#### **Problemas Encontrados y Soluciones**
1. **Definición de Fechas**:
   - Problema: Filtrar fechas basándose solo en mes y día.
   - Solución: Uso de `strftime` en consultas SQL.

2. **Integración de Tareas Programadas**:
   - Problema: APScheduler no ejecutaba tareas.
   - Solución: Inicializar el planificador correctamente en el contexto de Flask.

3. **Validación de Usuarios**:
   - Problema: Permitir solo usuarios mayores de 18 años.
   - Solución: Agregar validación en el registro utilizando la diferencia de fechas.

#### **Resultados**
- Formulario de registro funcional.
- Emails manuales enviados correctamente en pruebas.
- Configuración básica del administrador.

---

### **Etapa 2: Iteraciones y Mejoras**

#### **Hitos Alcanzados**
1. **Interfaz Administrativa**:
   - Panel con pestañas:
     - Cumpleaños del día.
     - Búsqueda de usuarios.
     - Agregar usuarios.
   - Funcionalidades de redención de obsequios.

2. **Automatización del Envío de Emails**:
   - Emails de recordatorio programados para el 1 y 16 de cada mes.
   - Emails de felicitación enviados el día exacto del cumpleaños.

3. **Optimizaciones Visuales**:
   - Uso de Bootstrap para mejorar el diseño.
   - Implementación de tema oscuro.

#### **Problemas Encontrados y Soluciones**
1. **Circular Imports**:
   - Problema: Los archivos de configuración causaban errores al importar.
   - Solución: Reestructurar las importaciones y modularizar las funciones.

2. **Error en el Envio de Emails**:
   - Problema: `mail` no definido en el contexto de tareas.
   - Solución: Configurar `Flask-Mail` en el contexto global correctamente.

3. **Falta de Logs**:
   - Problema: Dificultad para depurar errores en el envio de correos.
   - Solución: Implementar registros detallados con `logging`.

#### **Resultados**
- Administrador funcional con tareas manuales para pruebas.
- Correos automáticos configurados correctamente.
- Panel administrativo mejorado con funciones avanzadas.

---

### **Lecciones Aprendidas**
1. **Planificación**: Definir desde el principio los casos de uso y las funcionalidades esenciales.
2. **Modularización**: Evitar dependencias circulares segmentando lógica en módulos.
3. **Pruebas Contínuas**: Validar cada cambio en un entorno controlado antes de implementarlo.

---

### **Próximos Pasos**
1. Mejorar la documentación del proyecto.
2. Implementar pruebas unitarias para funciones críticas.
3. Optimizar la seguridad de las contraseñas y el acceso administrativo.
4. Ampliar las funcionalidades del administrador:
   - Notificaciones de actividad.
   - Reportes detallados de envíos.
5. Integrar soporte para idiomas adicionales.

---

Esta bitácora será actualizada a medida que el proyecto avance y se implementen nuevas mejoras.

# 11-01-2025

## Resumen de trabajo: Reestructuración de lógica y optimización de plantillas

**Fechas de trabajo:** [Incluir rango de fechas trabajado]

**Versiones alcanzadas:**

- `routes.py` v.1.2
- `ver_usuarios.html` v.1.2
- `admin.html` v.1.3
- `login.html` v.1.0
- `registro-cumples.html` v.1.0

### 1. Actualizaciones clave en `routes.py` (v.1.2):

**Manejo de usuarios:**

- Actualización de la ruta `/borrar-usuarios` para admitir eliminación en lote (batch) mediante método POST con datos JSON.
- Validación robusta para detectar IDs ausentes o solicitudes mal formadas.
- Manejo de errores detallado para facilitar el debugging.

**Consulta de usuarios:**

- Rutas funcionales para:
  - Obtener los usuarios actuales (`/ver-usuarios`).
  - Buscar usuarios en tiempo real con filtros avanzados (`/buscar-usuarios`).

**Optimización general:**

- Validación y manejo detallado de excepciones en todas las rutas críticas.
- Limpieza de código redundante.

### 2. Actualizaciones clave en plantillas:

#### 2.1. `admin.html` (v.1.3):

**Tabs completamente funcionales:**

- **Cumpleaños del día:** Carga de datos desde la base, alternando entre vistas de tabla y tarjeta.
- **Consulta de usuarios:** Búsqueda en tiempo real con soporte para filtros y vistas.
- **Agregar cumpleaños:** Validaciones completas, manejo de mensajes de error y éxito.

**Mejoras generales:**

- Compatibilidad Mobile First aplicada parcialmente, lista para ajustes finales de diseño.
- Conexión establecida con todas las rutas relevantes.

**Pendientes:**

- Mejorar UX/UI y selector de tema.
- Validar botones para pruebas de envío de correos.

#### 2.2. `ver_usuarios.html` (v.1.2):

**Vista responsiva:**

- Uso de contenedor `<div class="table-responsive">` para asegurar el diseño Mobile First.
- Compatibilidad con pantallas pequeñas para tablas grandes.

**Gestión de acciones:**

- Implementación de botón para eliminar usuarios seleccionados (batch delete).
- Restauración del botón de eliminación individual con funcionalidad completa.

**Validaciones:**

- Validación visual y funcional de los checkboxes de selección múltiple.

**Campos adicionales:**

- Inclusión de la columna "Apodo" en la tabla de usuarios.

**Mensajes de confirmación:**

- Alertas claras tras la eliminación exitosa o en caso de errores.

#### 2.3. `login.html` (v.1.0):

**Diseño básico funcional:**

- Formulario con campos para nombre de usuario y contraseña.
- Manejo de mensajes de error en caso de credenciales incorrectas.

**Compatibilidad responsiva:**

- Estilo sencillo y adaptable a pantallas pequeñas.

#### 2.4. `registro-cumples.html` (v.1.0):

**Formulario validado:**

- Campos obligatorios para nombre, correo electrónico y fecha de nacimiento.
- Campo opcional para apodo.

**Manejo de errores:**

- Mensajes específicos para edad no válida (<18 años) o correo duplicado.
- Manejo de excepciones con alertas claras.

**Conexión con la base de datos:**

- Validación y registro correcto en la base de datos.

**Mensajes de éxito:**

- Visualización en pantalla tras el registro exitoso.

### 3. Estado actual del sistema:

**Funcionalidades clave completas:**

- Las tres tabs de `admin.html` funcionan correctamente.
- Consulta y eliminación de usuarios en tiempo real desde `ver_usuarios.html`.
- Registro de cumpleaños validado con errores específicos en `registro-cumples.html`.
- Inicio y cierre de sesión funcional desde `login.html`.

**Responsividad:**

- Diseño adaptativo aplicado a todas las plantillas, asegurando compatibilidad con dispositivos móviles.

**Pendientes:**

- **Correos automáticos:** Validar envío y conexión con botones de prueba en `admin.html`.
- **UX/UI:** Ajustes finales de diseño para todas las plantillas.
- **Selector de tema:** Implementar soporte completo para modo claro/oscuro.

### Conclusión:

El sistema está funcional y preparado para las siguientes etapas:

- Validación de lógica de correos automáticos.
- Ajustes finales de diseño y experiencia de usuario.
- Pruebas generales previas a la etapa de producción.

## 12-01-2025

### Chagelog

**__init__.py**
- v.1.1
    - se crea el objeto Mail
    - se agrega de manera temporal un bloque de prints para probar la configuración de email

**routes.py**
- v.1.3
    - se importa el objeto mail directamente de la app
    - se configuran los logs

**.env**
- v.1.1
    - Se agregan credenciales de gmail, para testting, en vez de las propias del server de theend.com.uy

**run.py**
- v.1.1
    -   Se cambia el código de run.py para asegurarse de que .env se cargue desde el lugar correcto:
- v.1.2
    - se agrega otro tipo de carga de .env

**settings.py**
- v.1.2
    - Se actualiza para verificar que seestás usando os.getenv en todas las configuraciones para que Flask lea correctamente las variables del entorno:

### Se revierten todos los cambios al último commit

- a solucionar plantilla agregar cumpleaños: mensajes personalizados
- a solucionar plantilla admin: no realiza búsqueda

**settings.py**
- v.1.3
    - Se genera una nueva versión para asegurar que las configuraciones se carguen correctamente y evitar problemas futuros
      - Usar rutas relativas para la base de datos
      - Validación automática de las configuraciones de correo
      - Manejo robusto de valores booleanos desde el entorno
      - Mensajes claros en caso de errores

**run.py**
- v.1.4
    -   se limpia para que solo maneje la ejecución de la app

**__init__.py**
- v.1.2
    - Validación de configuraciones de correo electrónico
    - Mensajes de error amigables
    - Sin romper otras funcionalidades

**.env**
- v.1.2
    - Se agregan credenciales de gmail, para testting, en vez de las propias del server de theend.com.uy

**routes.py**
- v.1.4
    - se agrega una ruta temporal para prueba de envío de correos

**test_task.py**
- v.1.0
    - se crea para probar manualmente las tareas de envío de correo
    - se agrega código para  para ajustar dinámicamente el PYTHONPATH
- v.1.1
    - se corrigen las importaciones dede emails_utils,py
- v.1.2
    - se agrega la creación de una instancia de la app
- v.1.3
    - se agrega un bloque  para confirmar si las variables del archivo .env están siendo cargadas
    - se agrega dinámicamente el directorio raíz al PYTHONPATH

**task.py**
- v.1.2 
   - Se corrige error de importación nombres incorrectos "enviar_recordatorios" y "enviar_saludos_cumpleanios", por "enviar_correos_recordatorio" y "enviar_correos_cumpleaños"


## Prueba de tareas programadas de envío de correos EXITOSAS!!!

**routes.py**
- v.1.5
   - Añadida lógica para enviar un correo de confirmación al registrar un nuevo usuario.
   - Uso de la plantilla registrook.html para el correo de registro exitoso.

**run.py**
- v.1.5
   - Implementada validación robusta de la configuración de correo con Config.validate_email_config.
   - Depuración opcional de variables de entorno en modo DEBUG al inicio del archivo.
   - Confirmación visual de validación exitosa de configuraciones de correo.
   - settings.py
- v.1.4
   - Se mantiene la validación de configuraciones de correo con mensajes detallados para identificar errores rápidamente.

**registrook.html**
- v.1.0 (NUEVO)
   - Plantilla HTML para el correo de confirmación de registro exitoso.
   - Contenido inicial básico para informar al usuario del registro satisfactorio.
 
 ### Tareas realizadas
   - Envío de correos de confirmación de registro exitoso:

1. Integración en la ruta /agregar-cumple.
      * Verificación funcional del envío de correos desde el formulario de registro.
      * Uso de la nueva plantilla registrook.html.
2. Validación de configuraciones de correo:
      * Mecanismo robusto para evitar problemas al iniciar la app por configuraciones faltantes.
      * Confirmación visual de configuraciones exitosas.
3. Depuración de variables de entorno:
      * Depuración opcional en modo DEBUG para facilitar el rastreo de errores.

## 12-01-2025
### Chagelog

**routes.py (v.2.1)**
   - Ruta para ordenar usuarios según registros más recientes o antiguos.
   - Mejoras en la lógica de filtrado y manejo de datos.
**ver_usuarios.html (v.1.7):**
   - Añadido selector de orden de usuarios.
   - Scripts para cargar dinámicamente usuarios en orden ascendente o descendente.
   - Soluciones a botones de borrado, selección múltiple y vistas en tarjetas.
   - Actualizaciones para sincronización con el selector de orden.
**models.py (v.1.2):**
   - Agregada columna fecha_registro con soporte para zona horaria.
**run.py (v.1.7):**
   - Integración con Flask-Migrate para manejar cambios en la base de datos.
**settings.py (v.1.4):**
   - Ajuste para sincronizar con las herramientas de migración.
**Nueva Carpeta:**
**migrations:**
   - Contiene el historial de cambios aplicados a la base de datos mediante Flask-Migrate.
   - Generada automáticamente para reflejar las modificaciones de la columna fecha_registro.
1. Nuevas Funcionalidades:
      * Orden dinámico de usuarios por fecha de registro.
      * Selección de múltiples usuarios para borrado.
      * Botón de borrado individual funcionando correctamente.
      * Vista en tarjetas sincronizada con datos de usuarios.
      * Registro automático de la fecha de creación al añadir un nuevo usuario.
2. Cambios Generales:
      * Configuración de Flask-Migrate para manejar cambios futuros en la base de datos.
      * Mejora del flujo de navegación y manejo de errores en las vistas y rutas.
      * Validación y visualización de datos más robusta en todas las interfaces.

# Bitácora de Desarrollo - CumpleApp

## **Hito Alcanzado: Módulo de Correos (mC) Funcional**  
**Fecha:** 2025-01-14  
**Versión:** mC v.1.0.0  

### **Descripción General**
El módulo de correos (mC) está ahora completamente funcional. Todas las tareas relacionadas con el envío de correos electrónicos han sido configuradas y probadas con éxito, incluyendo correos de prueba, recordatorios y saludos de cumpleaños. Los correos están llegando correctamente a sus destinatarios, marcando un avance significativo en el desarrollo del sistema.

---

### **Cambios Realizados**
1. **Configuración del Correo:**
   - Validación y carga correcta de las variables desde el archivo `.env`:
     - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`
     - `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`
   - Comprobación y depuración de la configuración desde `__init__.py`.

2. **Actualización de Tareas Programadas (`tasks.py`):**
   - Uso explícito del contexto de la aplicación (`app_context`) para las tareas programadas.
   - Implementación de logs para rastrear próximas ejecuciones y estados de las tareas:
     - Recordatorios de cumpleaños (enviados 7 días antes).
     - Saludos de cumpleaños (enviados el día del cumpleaños).

3. **Corrección de Funciones de Envío (`email_utils.py`):**
   - Ajustes en las funciones `enviar_correos_recordatorio` y `enviar_correos_cumpleaños`:
     - Validación de usuarios y plantillas antes del envío.
     - Uso correcto de `MAIL_DEFAULT_SENDER` para evitar errores de remitente.

4. **Pruebas Manuales Realizadas:**
   - Ejecución de tareas programadas a través de botones de prueba en la interfaz de administración.
   - Configuración temporal de las tareas para ejecuciones inmediatas, simulando fechas reales.
   - Confirmación de entrega de correos con los siguientes resultados:
     - **Correos enviados correctamente:** Los destinatarios recibieron los correos de prueba, recordatorios y saludos.
     - **Errores menores registrados:** Algunos logs muestran errores relacionados con el remitente (`default@domain.com`), pero los correos llegan correctamente.

---

### **Pendientes/Incidencias Menores**
1. **Depuración de Logs y Mensajes de Error:**
   - Los logs actuales incluyen referencias a `default@domain.com` que deben eliminarse.
   - Refinar los mensajes de error para mejorar el debugging.

2. **Consistencia de Pruebas Manuales y Tareas Programadas:**
   - Verificar que todas las pruebas sigan el mismo flujo que las tareas programadas.
   - Validar que las plantillas usadas en los correos estén alineadas con las configuraciones finales.

---

### **Acciones Próximas**
- Realizar un commit estable con la versión actual del mC.
- Continuar con la integración del mC con el módulo de Usuarios (mU) si es necesario.
- Revisar y optimizar otros módulos o funcionalidades relacionadas.

---

**¡Hito logrado!** El sistema cumple con los requisitos funcionales del módulo de correos. Ahora estamos en condiciones de avanzar hacia la mejora de otros módulos o áreas del proyecto.

**Hito conseguido** Se ajustó el campo de búsqueda en admin.html
y el from de los correo en settings.py v1.5 y en "__init__.py" v1.8