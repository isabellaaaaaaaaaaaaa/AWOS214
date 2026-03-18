#Paso 6 Asi queda el main solo para levantar la api y listar los endpoints de los routers
#Y para eso hay que importar dichos routers y llamarlos
#Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios

# Instancia del servidor
app = FastAPI(
    title="Mi primer API",
    description="Isabella Castro Alavez",
    version="1.0.0"
)

app.include_router(usuarios.router)
app.include_router(varios.router)
