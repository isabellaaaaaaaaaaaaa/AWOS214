from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API sistema de tickets de soporte técnic"
)


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
 