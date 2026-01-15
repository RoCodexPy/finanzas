from fastapi import APIRouter, Depends, HTTPException
from ..models import Transaccion, Tipo, Categoria, Metodo_Pago
from sqlmodel import Session
from ..database import get_session
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post('/transacciones/')
def crear_transaccion(transaccion: Transaccion, session:Session = Depends(get_session)):

    
    tipo_db=session.get(Tipo,transaccion.tipo_id)
    categoria_db = session.get(Categoria, transaccion.categoria_id)
    metodo_db = session.get(Metodo_Pago, transaccion.metodo_pago_id)


    if tipo_db and tipo_db.nombre=="gasto":
        if transaccion.categoria_id == None:
            raise HTTPException(status_code=400,detail="Los gastos deben tener una categoría")
        elif categoria_db is None:
            raise HTTPException(status_code=404, detail="No existe una categoría con ese id")

    if tipo_db is None:
        raise HTTPException(status_code=404, detail=f"No existe un tipo de transaccion con ese id")
        
    if metodo_db is None:
        raise HTTPException(status_code=404, detail="No existe un metodo de pago con ese id")

    if transaccion.monto < 0:
        raise HTTPException(status_code=400, detail="El monto no puede ser menor a 0")


    try:
        session.add(transaccion)
        session.commit()
        session.refresh(transaccion)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='La transaccion ya existe')
        

    return transaccion

@router.get("/{transaccion_id}",response_model=Transaccion)
def get_transaccion(transaccion_id: int, session: Session = Depends(get_session)):
    transaccion_db = session.get(Transaccion, transaccion_id)

    if transaccion_db is None:
        raise HTTPException(
            status_code=404,
            detail="No existe una transaccion con ese id"
        )
    
    return  transaccion_db