# IMPORTACIONES 

# Importa la clase principal para crear la API
# status = códigos de respuesta HTTP (200, 404, etc)
# HTTPException = sirve para lanzar errores HTTP
# Depends = sirve para dependencias (ej: autenticación)
from fastapi import FastAPI, status, HTTPException, Depends

# Librería para trabajar con funciones asíncronas (simular espera)
import asyncio

# Permite usar tipos opcionales (variables que pueden ser None)
from typing import Optional

# BaseModel sirve para crear modelos de datos con validación automática
# Field permite agregar reglas de validación
from pydantic import BaseModel, Field 

# Librerías para autenticación básica
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Librería para comparar strings de forma segura (evita ataques)
import secrets



# INSTANCIA DEL SERVIDOR 

# Aquí se crea la aplicación FastAPI
app = FastAPI(

    # Título que aparece en la documentación automática
    title="Mi primer API",

    # descripción de la API
    description="Isabella Castro Alavez",

    # versión de la API
    version="1.0.0"
)



# BASE DE DATOS FICTICIA 

# Lista que simula una base de datos
# Cada elemento es un diccionario que representa un usuario
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre":"Abdiel", "edad" :21 },
    {"id": 4, "nombre":"Jafet", "edad" :24 },
    {"id": 5, "nombre":"Roger", "edad" :19 },
]



# MODELO DE VALIDACIÓN

# Se crea una clase que define cómo debe verse un usuario
# FastAPI usará esto para validar automáticamente los datos
class usuario_create(BaseModel):

    # id obligatorio (...) y debe ser mayor a 0
    id: int = Field(...,gt=0, description="Identificador de usuario")

    # nombre obligatorio con longitud entre 3 y 50 caracteres
    nombre:str=  Field(..., min_length=3, max_length=50, example="Juanita")

    # edad entre 1 y 123
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")



# SEGURIDAD HTTP BASIC 

# Se crea el sistema de seguridad HTTP Basic
security = HTTPBasic()


# Función que verifica las credenciales del usuario
def verificar_Peticion(credenciales: HTTPBasicCredentials = Depends(security)):

    # Compara el username recibido con el esperado
    userAuth = secrets.compare_digest(credenciales.username, "IsabellaCastro")

    # Compara el password recibido con el esperado
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    # Si alguno es incorrecto
    if not (userAuth and passAuth):

        # lanza un error 401 (no autorizado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )

    # si todo es correcto devuelve el username
    return credenciales.username



# ENDPOINTS 


# Endpoint GET básico
# Ruta principal de la API
@app.get("/", tags=["Inicio"])

async def bienvenido():

    # Devuelve un JSON
    return {"Mensaje": "Bienvenido a mi API"}



# Endpoint asincrono
# Simula una carga lenta
@app.get("/Hola Mundo", tags=["Bienvenida Asincrona"])

async def Hola():

    # espera 7 segundos
    await asyncio.sleep(7)

    # respuesta
    return {"Mensaje": "Bienvenido a mi API"}



# PARAMETRO OBLIGATORIO

# Endpoint con parámetro obligatorio en la URL
# Ejemplo: /v1/usuario/3
@app.get("/v1/usuario/{id}", tags=["Parametro Obligatorio"])

async def consultaUno(id: int):

    return {"Se encontro usuario": id}



# PARAMETRO OPCIONAL

# Endpoint donde el parámetro id es opcional
@app.get("/v1/usuarios/", tags=["Parametro Opcional"])

async def consultaTodos(id: Optional[int] = None):

    # si se envió id
    if id is not None:

        # busca en la lista
        for usuario in usuarios:

            if usuario["id"] == id:

                return {
                    "mensaje": "usuario encontrado",
                    "usuario": usuario
                }

        # si no lo encuentra
        return {
            "mensaje": "usuario no encontrado",
            "usuario": id
        }

    else:

        # si no se mandó id
        return {
            "mensaje": "No se proporcionó id"
        }



# CRUD: LEER USUARIOS

# Devuelve todos los usuarios
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])

async def leer_usuarios():

    return {
        "status": "200",
        "total": len(usuarios),  # cantidad de usuarios
        "usuarios": usuarios
    }



#CRUD: CREAR USUARIO

# POST sirve para crear datos
@app.post("/v1/usuarios/", tags=["CRUD HTTP"])

async def crear_usuario(usuario: usuario_create): 

    # verifica que el id no exista
    for usr in usuarios:

        if usr["id"] == usuario.id: 

            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    # agrega el usuario a la lista
    usuarios.append(usuario)

    return {
        "mensaje": "Usuario agregado",
        "Usuario": usuario
    }



# CRUD: ACTUALIZAR

# PUT se usa para actualizar datos
@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])

async def actualizar_usuario(id: int, usuario: dict):

    # asegura que el id del body sea el mismo de la URL
    usuario["id"] = id
    
    # busca el usuario
    for i in range(len(usuarios)):

        if usuarios[i]["id"] == id:

            # reemplaza el usuario
            usuarios[i] = usuario

            return {
                "mensaje": "Usuario actualizado",
                "Usuario": usuario
            }

    # si no existe
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )



# CRUD: ELIMINAR

# DELETE elimina usuarios
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)

async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):

    # busca el usuario
    for usuario in usuarios:

        if usuario["id"] == id:

            # elimina el usuario de la lista
            usuarios.pop(index)

            return{
                "messege":f"Usuario eliminado por: {userAuth}"
            }

    # si no existe
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )