from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..database import get_session
from ..models import Transaccion, Tipo, Metodo_Pago, Categoria
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix='/config', tags=["Configuracion"])


@router.post('/tipo_transaccion/')
def crear_tipo_transaccion(tipo: Tipo, session: Session = Depends(get_session)):
    try:
        session.add(tipo)
        session.commit()
        session.refresh(tipo)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al crear")
    
@router.post('/metodo_pago/')
def crear_metodo_pago(metodo: Metodo_Pago, session: Session = Depends(get_session)):
    try:
        session.add(metodo)
        session.commit()
        session.refresh(metodo)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al crear")


@router.post('/categoria/') #categorias para clasificar los gastos
def crear_categoria(categoria: Categoria, session: Session = Depends(get_session)):
    try:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al crear")
