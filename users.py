from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Simular una base de datos
users_list = [User(id=1, name="A", surname="AA", url="https://a.dev", age=30),
              User(id=2, name="B", surname="BB", url="https://b.dev", age=32),
              User(id=3, name="C", surname="CC", url="https://c.dev", age=33)]

###  CRUD  ####
@app.get("/users")
async def get_users():
    return users_list

@app.get("/user/{id}")
async def get_user(id: int):
    return search_user(id)
    
@app.post("/user/")
async def add_user(user: User):
    # Comprobar si ya hay un usuario en la lista
    if type(search_user(user.id)) == User: # Si devuelve un usuario con el mismo id
        return {"error": "Usuario ya está añadido en la BD."}
    users_list.append(user)
    return {"success": f"Usuario {user.id} añadido correctamente."}

@app.put("/user/")
async def update_user(user: User):
    for index, new_user in enumerate(users_list):
        if new_user.id == user.id:
            users_list[index] = user
            return {"success": f"Usuario {user.id} actualizado correctamente."}
    return {"error": "Usuario no existe en BD."}

@app.delete("/user/{id}")
async def delete_user(id: int):
    for index, new_user in enumerate(users_list):
        if new_user.id == id:
            del users_list[index]
            return {"success": f"Usuario {id} borrado correctamente."}
    return {"error": "Usuario no existe en BD."}
 
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Usuario no encontrado."}
