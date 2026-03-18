from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API sistema de tickets de soporte técnic"
)

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

@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi API"}

#listar
@app.get("/tickets")
def listar_libros():
    return libros

#consulta de id
@app.get("tickets/{id}", tags=["API sistema de tickets de soporte técnic"])

async def consultaUno(id: int):

    return {"Se encontro ticket": id}
    
#crear
@app.post("/v1/tickets/", tags=["API sistema de tickets de soporte técnico"])
async def crear_tickets(tickets: tickets_create): 

    for tickets in tickets:

        if tickets ["id"] == tickets.id: 

            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    tickets.append(tickets)

    return {
        "mensaje": "Ticket agregado",
        "Tickets":tickets
    }


#actualizacion de estado
@app.put("/v1/tickets/{id}", tags=["API sistema de tickets de soporte técnic"])

async def actualizar_tickets(id: int, tickets dict):
    tickets["id"] = id
    for i in range(len(tickets)):
        if tickets[i]["id"] == id:
            tickets[i] = tickets
            return {
                "mensaje": "Ticket actualizado",
                "tickets": tickets
            }
    raise HTTPException(
        status_code=404,
        detail="Ticket no encontrado"
    )

#delete
@app.delete("/v1/ticktes/{id}", tags=['API sistema de tickets de soporte técnic'], status_code=status.HTTP_200_OK)

async def eliminar_ticket(id:int, userAuth:str= Depends(verificar_Peticion)):

    for tickets in tickets:

        if tickets["id"] == id:

            tickets.pop(index)

            return{
                "messege":f"tickets eliminado por: {userAuth}"
            }

    raise HTTPException(
        status_code=400, 
        detail="Ticket no encontrado"
    )
 


#tickets = [
 #   {"nombre":"Ticket1",  "descripcion": "Este es un ticket", "prioridad":"alta", "estado":"pendiente"}
#]

c#lass tickets_create(BaseModel):
  #  nombre:str= Field(...,min_lenght=5)
   # descripcion:str= Field(..., min_lenght=20, max_lenght=200)
    #prioridad:str= FIeld (..., pattern="^(baja|media|alta)$")