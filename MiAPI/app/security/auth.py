#Paso 3 creamos carpeta de security y el archivo auth.py
#Seguridad HTTP Basic 
#Nos traemos la importaciones de security porque ningun otro archivo las usa solo auth y agregamos la de fastapi

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

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
