#Paso 4 creamos carpeta roiterd y archivo usuario
# mismo principio que los modelos de pydantic se establece que por entidad o tablas principales se dividen por "routers"
#Aqui pusimos los endpoints usuarios

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create #necesitamos los imports de el modelo de pydantic
from app.data.database import usuarios # import de los datos de la bd
from app.security.auth import verificar_Peticion #imports de la seguridad de nuetsra api

#Cons las importaciones actuales los app.gets nos dan error por la intsancia del sefvidor, entonces ponemos el importa de apirouter 
# para crear la "instancia en este archivo
#Así cambiamos cada app por router, esta funciona con pregijos y etiquetas, lo que todos los enponitns tiene en comun es su prefijo, 
# ya que este ahi ya no es necesario ponerlo en los enponints
router = APIRouter(
    prefix= "/v1/usuarios", tags={"CRUD HTTP"}
)

@router.get("/")
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
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

@router.put("/{id}", status_code=status.HTTP_200_OK)
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

@router.delete("/{id}", status_code=status.HTTP_200_OK)
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

