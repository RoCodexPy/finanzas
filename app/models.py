from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class TransaccionBase(SQLModel):
    monto: float = Field(gt=0, description="El monto debe ser mayor que 0")
    descripcion: str
    fecha: datetime 
    categoria_id: Optional[int]
    tipo_id: int
    metodo_pago_id: int

class Transaccion(TransaccionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float
    descripcion: str
    fecha: datetime = Field(default_factory=datetime.now)
    categoria_id: Optional[int] = Relationship() # en que se gasta o de donde ingresa
    tipo_id: int = Field(foreign_key="tipo.id") # Ingreso o gasto
    metodo_pago_id: int = Field(foreign_key="metodo_pago.id") # efectivo o tarjeta (o algun otro metodo)

class TransaccionCreate(TransaccionBase):
    pass


class CategoriaBase(SQLModel):
    nombre : str

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    nombre: str = Field( index=True, unique=True)

class TipoBase(SQLModel):
    nombre: str

class Tipo(TipoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)


class Metodo_PagoBase(SQLModel):
    nombre: str

class Metodo_Pago(Metodo_PagoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)


