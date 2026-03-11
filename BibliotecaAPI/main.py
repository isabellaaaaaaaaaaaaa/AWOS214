# -----------------------------
# IMPORTACIONES
# -----------------------------
# FastAPI: framework para crear APIs en Python
# status: permite usar códigos HTTP estándar (200, 404, etc.)
# HTTPException: sirve para lanzar errores HTTP personalizados
# Depends: permite usar dependencias como autenticación

from fastapi import FastAPI, status, HTTPException, Depends

# asyncio se usa para simular procesos asincrónicos
import asyncio

# Optional permite que un parámetro sea opcional
from typing import Optional

# BaseModel y Field se usan para validar datos de entrada
from pydantic import BaseModel, Field 

# HTTPBasic permite autenticación básica (usuario y contraseña)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# secrets se usa para comparar contraseñas de forma segura
import secrets



# INSTANCIA DEL SERVIDOR

# Aquí se crea la aplicación de FastAPI.
# Estos datos aparecerán en la documentación automática (/docs).

app = FastAPI(
    title="Mi primer API",
    description="Isabella Castro Alavez",
    version="1.0.0"
)



# BASE DE DATOS FICTICIA

# Esta es una lista de usuarios simulando una base de datos.
# En proyectos reales se conectaría a MySQL, PostgreSQL, MongoDB, etc.

usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre":"Abdiel", "edad" :21 },
    {"id": 4, "nombre":"Jafet", "edad" :24 },
    {"id": 5, "nombre":"Roger", "edad" :19 },
]


# MODELO DE VALIDACIÓN

# Este modelo define cómo debe ser un usuario al crearse.
# FastAPI validará automáticamente los datos que lleguen en el body.

class usuario_create(BaseModel):

    # ID obligatorio mayor a 0
    id: int = Field(...,gt=0, description="Identificador de usuario")

    # Nombre obligatorio entre 3 y 50 caracteres
    nombre:str=  Field(..., min_length=3, max_length=50, example="Juanita")

    # Edad entre 1 y 123
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")



# SEGURIDAD HTTP BASIC

# Se crea un sistema de autenticación simple.

security = HTTPBasic()

def verificar_Peticion(credenciales: HTTPBasicCredentials = Depends(security)):

    # Se comparan las credenciales ingresadas con las definidas
    userAuth = secrets.compare_digest(credenciales.username, "IsabellaCastro")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    # Si no coinciden, se lanza un error de autorización
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )

    # Si son correctas se devuelve el nombre de usuario autenticado
    return credenciales.username


# ENDPOINTS


# Endpoint raíz
# Se usa para verificar que la API está funcionando
@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"Mensaje": "Bienvenido a mi API"}


# Endpoint asincrónico
# Simula una carga o proceso largo usando asyncio.sleep
@app.get("/Hola Mundo", tags=["Bienvenida Asincrona"])
async def Hola():

    # simula espera de 7 segundos
    await asyncio.sleep(7)

    return {"Mensaje": "Bienvenido a mi API"}


# Endpoint con parámetro obligatorio
# El ID se pasa en la URL
# ejemplo: /v1/usuario/3
@app.get("/v1/usuario/{id}", tags=["Parametro Obligatorio"])
async def consultaUno(id: int):

    return {"Se encontro usuario": id}


# Endpoint con parámetro opcional
# Se pasa como query parameter
# ejemplo:
# /v1/usuarios/buscar?id=3

@app.get("/v1/usuarios/buscar", tags=["Parametro Opcional"])
async def consultaTodos(id: Optional[int] = None):

    # Si se proporciona ID se busca el usuario
    if id is not None:

        for usuario in usuarios:

            if usuario["id"] == id:
                return {
                    "mensaje": "usuario encontrado",
                    "usuario": usuario
                }

        # si no se encuentra
        return {
            "mensaje": "usuario no encontrado",
            "usuario": id
        }

    else:

        return {
            "mensaje": "No se proporcionó id"
        }


# Endpoint para leer todos los usuarios
# Método GET del CRUD
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuarios():

    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


# Endpoint para crear un usuario
# Método POST del CRUD
@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario(usuario: usuario_create): 

    # Se verifica que el ID no exista
    for usr in usuarios:

        if usr["id"] == usuario.id: 

            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    # Se agrega el usuario a la lista
    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado",
        "Usuario": usuario
    }


# Endpoint para actualizar un usuario
# Método PUT del CRUD
@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):

    # Se asegura que el ID del body sea el mismo que el de la URL
    usuario["id"] = id
    
    for i in range(len(usuarios)):

        if usuarios[i]["id"] == id:

            usuarios[i] = usuario

            return {
                "mensaje": "Usuario actualizado",
                "Usuario": usuario
            }
    
    # si no se encuentra el usuario
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# Endpoint para eliminar usuario
# Método DELETE del CRUD
# Este endpoint requiere autenticación

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):

    # Se busca el usuario por ID
    for index, usuario in enumerate(usuarios):

        if usuario["id"] == id:

            usuarios.pop(index)

            return{
                "messege":f"Usuario eliminado por: {userAuth}"
            }

    # si no existe
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )