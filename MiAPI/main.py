#Importancionescd..
from fastapi import FastAPI

#nuevaaa 
import asyncio 

#Intstancia del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi APi"}

@app.get("/Hola Mundo")
async def Hola():
    await asyncio.sleep(7) #simular como si estuviera cargandi 

    return {"Mensaje": "Bienvenido a mi APi"}