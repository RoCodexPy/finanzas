# Copilot Instructions - Finanzas Project

## Project Overview
**Finanzas** is a financial transaction management API built with **FastAPI** and **SQLModel**. It tracks income and expenses with categories, transaction types, and payment methods.

## Architecture

### Core Components
- **`app/main.py`**: FastAPI application entry point with lifespan context manager that auto-initializes DB tables and seed data (Tipo, Categoria, Metodo_Pago)
- **`app/models.py`**: SQLModel data models using SQLAlchemy ORM
  - `Transaccion`: Main transaction entity (amount, description, date, category, type, payment method)
  - `Tipo`: Transaction type (ingreso/gasto - income/expense)
  - `Categoria`: Expense classification (comida, transporte, ropa, aseo, otros)
  - `Metodo_Pago`: Payment method (efectivo, transferencia)
- **`app/routes/`**: Modular route handlers with APIRouter
  - `transacciones.py`: CRUD operations for transactions with validation
  - `config.py`: Setup endpoints for types, categories, and payment methods
- **`app/database.py`**: SQLite connection engine and session dependency

### Data Flow
1. HTTP request → FastAPI route handler
2. Get session via `Depends(get_session)` dependency injection
3. Query/modify data using SQLModel with Tipo/Categoria/Metodo_Pago lookups
4. Commit to SQLite and return model instance
5. FastAPI auto-serializes response to JSON via Pydantic

## Key Patterns & Conventions

### Validation & Error Handling
- **Pre-commit validation**: Check foreign key existence (Tipo, Categoria, Metodo_Pago) before adding transactions
- **Business logic**: Expenses (tipo_id='gasto') require a categoria_id; incomes can be null
- **HTTP exceptions**: Use `HTTPException(status_code=..., detail=...)` for errors (400 for validation, 404 for not found)
- **Integrity errors**: Catch `IntegrityError` for duplicate entries

### Dependency Injection
All route handlers use `session: Session = Depends(get_session)` to get DB session. Never instantiate sessions manually.

### Model Structure
Use base classes for request schemas (e.g., `TransaccionBase`, `CategoriaBase`) and extend for table models:
```python
class TransaccionBase(SQLModel):
    monto: float = Field(gt=0)
    # ... common fields
class Transaccion(TransaccionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```

## Critical Files & Extension Points
- **Add new transaction endpoints**: Extend [routes/transacciones.py](routes/transacciones.py) - follow Tipo/Categoria validation pattern
- **Add new config types**: Extend [routes/config.py](routes/config.py) with similar post/get endpoints
- **Add models**: Define in [app/models.py](app/models.py) and seed in [app/main.py](app/main.py) lifespan if needed
- **Database changes**: Update [app/database.py](app/database.py) if switching databases

## Running & Development
- **Start server**: `uvicorn app.main:app --reload` (watch mode with uvloop)
- **Environment**: Python 3.11 with venv at `finanzas_venv/`
- **Dependencies**: FastAPI, SQLModel, Pydantic, uvicorn, watchfiles for live reload

## Common Tasks
- **Create transaction**: POST `/transacciones/transacciones/` - validates tipo_id, categoria_id, metodo_pago_id exist; enforces categoria required for expenses
- **Get transaction**: GET `/transacciones/{transaccion_id}`
- **Add category**: POST `/config/categoria/` with `{"nombre": "..."}`
- **Add type**: POST `/config/tipo_transaccion/` with `{"nombre": "ingreso"|"gasto"}`
- **Add payment method**: POST `/config/metodo_pago/` with `{"nombre": "..."}`
