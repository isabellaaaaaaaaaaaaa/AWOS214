# Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

# Instancia del servidor
app = FastAPI(
    title="Mi primer API",
    description="Isabella Castro Alavez",
    version="1.0.0"
)

# BD ficticia
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21}
]

# Endpoints
@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi API"}

@app.get("/Hola Mundo", tags=["Bienvenida Asincrona"])
async def Hola():
    await asyncio.sleep(7)  # simula carga
    return {"Mensaje": "Bienvenido a mi API"}

@app.get("/v1/usuario/{id}", tags=["Parametro Obligatorio"])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}

@app.get("/v1/usuarios/", tags=["Parametro Opcional"])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "mensaje": "usuario encontrado",
                    "usuario": usuario
                }
        return {
            "mensaje": "usuario no encontrado",
            "usuario": id
        }
    else:
        return {
            "mensaje": "No se proporcionó id"
        }
