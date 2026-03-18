#Paso 5 ahora creamos el "router" para los demas endpoints
# Endpoints varios
#Aqui no podemos usar ni un prefijo pq no hay nada que compartan los endpoints y lo mismo en las etiquetas
from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router= APIRouter(tags=['Varios'])

@router.get("/", tags=["Inicio"])
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi API"}

@router.get("/Hola Mundo", tags=["Bienvenida Asincrona"])
async def Hola():
    await asyncio.sleep(7)  # simula carga
    return {"Mensaje": "Bienvenido a mi API"}

@router.get("/v1/usuario/{id}", tags=["Parametro Obligatorio"])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}

