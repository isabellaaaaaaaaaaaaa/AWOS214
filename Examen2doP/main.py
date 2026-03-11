from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API sistema de tickets de soporte técnic"
)

tickets = [
    {nombre = "Ticket1",
    descripcion = "Este es un ticket de soporte tecnico para un sisitema de estos mismos",
    prioridad = "alta",
    estado = "pendiente"},
    {nombre = "Ticket2",
    descripcion = "Este es un ticket de soporte tecnico para un sisitema de estos mismos",
    prioridad = "media",
    estado = "pendiente"},
    {nombre = "Ticket3",
    descripcion = "Este es un ticket de soporte tecnico para un sisitema de estos mismos",
    prioridad = "baja",
    estado = "pendiente"}
]

class ticket_create(BaseModel):
    nombre:str= Field(...,min_lenght=5)
    descripcion:str= Field(..., min_lenght=20, max_lenght=200)
    prioridad:str= FIeld (..., pattern="^(baja|media|alta)$")

#seguridad
security = HTTPBasic()
def verificar_Peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")


    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )


    return credenciales.username

#endpoints
#listar
@app.get("/tickets")
def listar_libros():
    return libros
