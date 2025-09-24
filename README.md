# FastAPI + Uvicorn: Manual Paso a Paso

## Introducción
FastAPI es un framework web moderno y rápido para construir APIs con **Python 3.7+** basado en las **anotaciones** de tipos de Python. Uvicorn es un servidor ASGI ligero y rápido que se utiliza comúnmente para ejecutar aplicaciones FastAPI.

Las principales **características** de FastAPI son:

- Basado en **estándares** abiertos como OpenAPI y JSON Schema, y estándares de autenticación como OAuth2 y JWT.
  
- **Alto rendimiento**, comparable a NodeJS y Go (gracias a Starlette y Pydantic).
  
- **Rápido** de desarrollar, **con menos código y menos errores**.
  
- Soporte automático para **validación de datos**, serialización y **documentación interactiva**.
  
- **Fácil e intuitivo**, con una curva de aprendizaje suave.

## Requisitos previos

Antes de comenzar, asegúrate de tener **Python 3.7 o superior** instalado en tu sistema. También es recomendable crear un entorno virtual para tu proyecto.

Puedes crear un entorno virtual usando `venv`:

```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
```

## Instalación

Para instalar FastAPI y Uvicorn, puedes usar pip. Ejecuta el siguiente comando en tu terminal:

```bash
pip install "fastapi[all]" uvicorn
```

## Verificación de la instalación

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

El parámetro `--reload` hace que el servidor se **reinicie automáticamente** cuando detecta cambios en el código, lo cual es útil durante el desarrollo.

## Documentación automática

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación automática generada por FastAPI en tu navegador web. Tenemos 2 tipos de documentación automática en `FastAPI`:

- Documentación con **Swagger** -> http://127.0.0.1:8000/docs
  
- Documentación con **Redocly** -> http://127.0.0.1:8000/redoc

## Probar la API

Puedes probar la API utilizando herramientas como **Postman**, **Thunder Client** (extensión de VSCode) o incluso desde la propia documentación interactiva de Swagger.

## Autenticación y Autorización

FastAPI proporciona soporte integrado para la autenticación y autorización. Puedes utilizar **OAuth2, JWT** (JSON Web Token), o cualquier otro método de autenticación que prefieras. Consulta la [documentación oficial](https://fastapi.tiangolo.com/tutorial/security/) para más detalles.

Para instalar los paquetes para poder usar la autenticación JWT podemos instalar las siguientes librerías:

```bash
pip install pyjwt
pip install "passlib[bcrypt]"
```

**Bcrypt** es un algoritmo de hashing seguro que se utiliza comúnmente para proteger contraseñas. La biblioteca `passlib` proporciona una implementación fácil de usar de bcrypt y otros algoritmos de hashing.

## Bases de datos

`FastAPI` se puede integrar fácilmente con varias bases de datos utilizando ORM como SQLAlchemy, Tortoise ORM, o bases de datos NoSQL como MongoDB.  

- Consulta la [documentación oficial](https://fastapi.tiangolo.com/tutorial/sql-databases/) para más detalles.

Si deseas usar **SQLModel**, es una biblioteca que combina las características de **SQLAlchemy y Pydantic**, puedes instalarla junto con el conector de la base de datos que prefieras. 

A continuación dejo un enlace a la documentación oficial de SQLAlchemy para más detalles sobre los conectores disponibles.

- [SQLAlchemy Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html).

Es normal que nos encontremos muchas formas de conectarnos a una base de datos, por ejemplo MySQL que es la que usaremos en este manual, tiene varios conectores, como `mysqlclient`, `PyMySQL` o  `mysql-connector-python`, entre otros. 

Nosotros usaremos `PyMySQL` por su facilidad de instalación y uso.

- Documentación de [**PyMySQL**](https://pymysql.readthedocs.io/en/latest/user/installation.html)

Para instalar **SQLModel** y el conector de **MySQL**, puedes usar:

```bash
pip install sqlmodel 
pip install PyMySQL
```

Para PostgreSQL, puedes usar:

```bash
pip install sqlalchemy psycopg2
```

También es recomendable instalar `dotenv` para manejar variables de entorno para la configuración de la base de datos y otras configuraciones sensibles.

```bash
pip install python-dotenv
```

Una vez instalados los paquetes necesarios, puedes configurar la conexión a la base de datos en tu aplicación FastAPI.

La forma de conectarnos o crear el endpoint será de la siguiente manera:

```python
mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
```
Por ejemplo:

```python
DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
```



