#Clase para crear el motor de la bd
from sqlalchemy import create_engine
#Nos ayuda  crear sesciones
from sqlalchemy.orm import sessionmaker, declarative_base
#manipular el sistema operativo
import os

#Definir la url DE LA BD
DATABASE_URL = os.gettenv(
    "DATABASE_URL",
    #Conexion direcat a la aplicacion con el usuario, contraseña, puerto y bd a la que nos estamos conectabdo 
    "postgresql://admin:123456@postgres:5434/DB_miapi"
)

#CReanis el motor de conexion
engine= create_engine(DATABASE_URL)

#Creamos gestionador de sesiones, sirve para la gestion de la actualizacion que estaos haciendo, se crean en sesiones, ahorra lo de abrir y cerar sesiones
#Definimos tres parametris no se hace un cmabio si no lo autorizamos del orm, de los cambios, y le pasamos el motor creado
SesionLocal= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)