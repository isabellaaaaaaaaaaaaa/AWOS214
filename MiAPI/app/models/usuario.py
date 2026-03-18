#Paso 2 creamos carpeta de models y el archivo de usuario.py donde pegamos el modelo de validacion de pydantic
#Modelo de validación, le tenemos que agregar el import de pydantic sino da error

from pydantic import BaseModel, Field

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str=  Field(..., min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

