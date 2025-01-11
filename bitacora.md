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

