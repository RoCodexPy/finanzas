from fastapi import FastAPI, HTTPException, Depends
from .routes import config, transacciones
from datetime import datetime
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, select
from .models import Transaccion, Categoria, Tipo, Metodo_Pago
from .database import engine, get_session







@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)

    session = Depends(get_session)

    with Session(engine) as session:
        if not session.exec(select(Tipo)).first():
            session.add(Tipo(nombre='ingreso'))
            session.add(Tipo(nombre='gasto'))

        if not session.exec(select(Categoria)).first():
            session.add(Categoria(nombre='comida'))
            session.add(Categoria(nombre='transporte'))
            session.add(Categoria(nombre='ropa'))
            session.add(Categoria(nombre='aseo'))
            session.add(Categoria(nombre='otros'))

        if not session.exec(select(Metodo_Pago)).first():
            session.add(Metodo_Pago(nombre="efectivo"))
            session.add(Metodo_Pago(nombre="transferencia"))

        session.commit()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(config.router)
app.include_router(transacciones.router)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema Financiero Activo"}

