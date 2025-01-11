# Iniciador de la app v.1.0
from app import create_app
from app.tasks import iniciar_tareas

app = create_app()

if __name__ == '__main__':
    iniciar_tareas()  # Iniciar tareas programadas
    app.run(debug=True, host='0.0.0.0', port=5000)