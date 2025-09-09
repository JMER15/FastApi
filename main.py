from fastapi import FastAPI
from routers import products, users, basic_auth_user, jwt_auth_user

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a FastApi!"}