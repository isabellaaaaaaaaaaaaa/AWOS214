# Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

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
    {"id": 3, "nombre":"Abdiel", "edad" :21 },
    {"id": 4, "nombre":"Jafet", "edad" :24 },
    {"id": 5, "nombre":"Roger", "edad" :19 },
]

#Modelo de validación
class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str=  Field(..., min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")


# Seguridad HTTP Basic

security = HTTPBasic()
def verificar_Peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "IsabellaCastro")
    passAuth = secrets.compare_digest(credenciales.password, "123456")


    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )


    return credenciales.username

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

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario(usuario: usuario_create): 
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario agregado",
        "Usuario": usuario
    }

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):
    # Aseguramos que el ID en el body coincida con el de la URL
    usuario["id"] = id
    
    for i in range(len(usuarios)):
        if usuarios[i]["id"] == id:
            usuarios[i] = usuario
            return {
                "mensaje": "Usuario actualizado",
                "Usuario": usuario
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.pop(index)
            return{
                "messege":f"Usuario eliminado por: {userAuth}"
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )

