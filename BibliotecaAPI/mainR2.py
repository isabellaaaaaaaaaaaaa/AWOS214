from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI(
    title="API inventario",
    description="Sistema básico de gestión de productos",
    version="1.0"

)

materiales = [
    {"id" = "1",
    "nombre" = "Laptop",
    "preciio" = "2000",
    "stock" = "100"
    },
    {"id" = "2",
    "nombre" = "Mouse",
    "preciio" = "2000",
    "stock" = "100"
    },
    {"id" = "3",
    "nombre" = "Cable",
    "preciio" = "2000",
    "stock" = "100"
    },
    {"id" = "4",
    "nombre" = "Bocina",
    "preciio" = "2000",
    "stock" = "100"
    },
    {"id" = "5",
    "nombre" = "Bateria",
    "preciio" = "2000",
    "stock" = "100"
    }
]

#Validación id>0 nombre 3-50string precio>o stock>=0
class materiales_create(BaseModel):
    id= int = Field(...,gt=0, description="Identificadir de usuario")
    nombre:str= Field(..., min_lenght=3, max_lenght=50, description="Tu material para el inventario")
    precio= int =Field(..., gt=0, description="1000")
    stock= int = Field(..., ge=0, description="28")

@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi API"}

@app.get("productos/{id}", tags=["Parametro Obligatorio"])

async def consultaUno(id: int):

    return {"Se encontro usuario": id}
