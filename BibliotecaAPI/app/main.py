from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List

app = FastAPI(title="Api de Biblioteca Digital")

class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(..., pattern="^(disponible|prestado)$")


class Usuario(BaseModel):
    nombre: str
    correo: EmailStr


class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario

libros: List[Libro] = []
prestamos: List[Prestamo] = []

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l.id == libro.id:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un libro con ese ID"
            )

    libros.append(libro)
    return libro

@app.get("/libros")
def listar_libros():
    return libros

@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):

    for libro in libros:
        if libro.nombre.lower() == nombre.lower():
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:

        if libro.id == prestamo.libro_id:

            if libro.estado == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            libro.estado = "prestado"

            prestamos.append(prestamo)

            return {"mensaje": "Préstamo registrado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="El libro no existe"
    )

@app.put("/prestamos/{libro_id}", status_code=200)
def devolver_libro(libro_id: int):

    for prestamo in prestamos:

        if prestamo.libro_id == libro_id:

            prestamos.remove(prestamo)
            
            for libro in libros:
                if libro.id == libro_id:
                    libro.estado = "disponible"

            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo no existe"
    )

@app.delete("/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int):

    for prestamo in prestamos:

        if prestamo.libro_id == libro_id:
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado correctamente"}

    raise HTTPException(
        status_code=409,
        detail="El préstamo no existe"
    )