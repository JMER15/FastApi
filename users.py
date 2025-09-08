from fastapi import FastAPI, HTTPException
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
    if not users_list:
        raise HTTPException(status_code=404, detail="No hay usuarios en la BD.")
    return users_list

@app.get("/user/{id}")
async def get_user(id: int):
    user = search_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario {id} no encontrado.")
    return user

@app.post("/user/", status_code=201)
async def add_user(user: User):
    # Comprobar si ya hay un usuario en la lista
    if type(search_user(user.id)) == User: # Si devuelve un usuario con el mismo id
        raise HTTPException(status_code=409, detail="Usuario ya está añadido en la BD.") # 409 Conflict
    users_list.append(user)
    return {"success": f"Usuario {user.id} añadido correctamente."}

@app.put("/user/")
async def update_user(user: User):
    for index, new_user in enumerate(users_list):
        if new_user.id == user.id:
            users_list[index] = user
            return {"success": f"Usuario {user.id} actualizado correctamente."}
    raise HTTPException(status_code=404, detail=f"Usuario {user.id} no existe en BD.")

@app.delete("/user/{id}")
async def delete_user(id: int):
    for index, new_user in enumerate(users_list):
        if new_user.id == id:
            del users_list[index]
            return {"success": f"Usuario {id} borrado correctamente."}
    raise HTTPException(status_code=404, detail=f"Usuario {id} no existe en BD.")

# Función para buscar usuario por id 
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return None