## Instalación de FastAPI con Uvicorn

FastAPI es un framework web moderno y rápido para construir APIs con **Python 3.7+** basado en las **anotaciones** de tipos estándar de Python. Uvicorn es un servidor ASGI ligero y rápido que se utiliza comúnmente para ejecutar aplicaciones FastAPI.

### Requisitos previos

Antes de comenzar, asegúrate de tener **Python 3.7 o superior** instalado en tu sistema. También es recomendable crear un entorno virtual para tu proyecto.
Puedes crear un entorno virtual usando `venv`:

```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
```

### Instalación

Para instalar FastAPI y Uvicorn, puedes usar pip. Ejecuta el siguiente comando en tu terminal:

```bash
pip install "fastapi[all]" uvicorn
```

### Verificación de la instalación

Para verificar que FastAPI y Uvicorn se han instalado correctamente, puedes crear un archivo Python simple llamado `main.py` con el siguiente contenido:

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
```

Luego, ejecuta el servidor Uvicorn con el siguiente comando:

```bash
uvicorn main:app --reload # si esta añadido al PATH
```

sino usa:

```bash
python -m uvicorn main:app --reload
```

El parámetro `--reload` hace que el servidor se reinicie automáticamente cuando detecta cambios en el código, lo cual es útil durante el desarrollo.

### Documentación automática

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación automática generada por FastAPI en tu navegador web:

- Documentación con **Swagger** -> http://127.0.0.1:8000/docs
  
- Documentación con **Redocly** -> http://127.0.0.1:8000/redoc

### Probar la API

Puedes probar la API utilizando herramientas como **Postman**, **Thunder Client**.

### Autenticación y Autorización

FastAPI proporciona soporte integrado para la autenticación y autorización. Puedes utilizar OAuth2, JWT, o cualquier otro método de autenticación que prefieras. Consulta la [documentación oficial](https://fastapi.tiangolo.com/tutorial/security/) para más detalles.

Para instalar los paquetes para poder usar la autenticación JWT

```bash
pip install pyjwt
pip install "passlib[bcrypt]"
```

Bcrypt es un algoritmo de hashing seguro que se utiliza comúnmente para proteger contraseñas. La biblioteca `passlib` proporciona una implementación fácil de usar de bcrypt y otros algoritmos de hashing.



