from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configuración de la BD
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME")
}

DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Crear motor y sesión de la base de datos
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Generar una sesión sólo cuando se necesite y no tener muchas sesiones que pueden saturar la BD
def get_session(): 
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

class DriverF1Base(SQLModel):
    name: str
    team: str
    podiums: int = Field(ge=0)  # Validación para que no sea negativo
    win: int = Field(ge=0)

class DriverF1(DriverF1Base, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)

app = FastAPI()

# Evento de inicio para crear las tablas
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

##### CRUD Endpoints para pilotos F1 #####
@app.get("/drivers", response_model=List[DriverF1], status_code=status.HTTP_200_OK, tags=["F1 Drivers"]) # El response model es una lista de DriverF1
def get_drivers(session: session_dep):
    drivers = session.exec(select(DriverF1)).all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No hay pilotos en la base de datos.")
    return drivers


@app.get("/drivers/{driver_id}", response_model=DriverF1, status_code=status.HTTP_200_OK, tags=["F1 Drivers"])
def get_driver(driver_id: int, session: session_dep):
    driver = session.get(DriverF1, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Piloto no encontrado.")
    return driver


@app.post("/drivers", response_model=DriverF1, status_code=status.HTTP_201_CREATED, tags=["F1 Drivers"])
def create_driver(driver: DriverF1, session: session_dep):
    new_driver= session.exec(select(DriverF1).where(DriverF1.name == driver.name)).first() # Comprobar si ya existe el piloto
    if new_driver:
        raise HTTPException(status_code=409, detail="El piloto ya existe en la base de datos.")
    session.add(driver) # Añadir el nuevo piloto a la sesión
    session.commit()
    session.refresh(driver)
    return driver


@app.put("/drivers/{driver_id}", response_model=DriverF1, status_code=status.HTTP_200_OK, tags=["F1 Drivers"])
def update_driver(driver_id: int, updated_driver: DriverF1, session: session_dep):
    driver = session.get(DriverF1, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Piloto no encontrado.")
    driver.name = updated_driver.name
    driver.team = updated_driver.team
    driver.podiums = updated_driver.podiums
    driver.win = updated_driver.win
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return driver


@app.delete("/drivers/{driver_id}", status_code=status.HTTP_200_OK, tags=["F1 Drivers"])
def delete_driver(driver_id: int, session: session_dep):
    driver = session.get(DriverF1, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Piloto no encontrado.")
    session.delete(driver)
    session.commit()
    return {"ok": True}


