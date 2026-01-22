from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    age: int
    real: bool = True

app = FastAPI()

@app.post('/item/')
def create_item(item: Item):
    item = Item(name='elemento creado', age=15, real=True)
    return item

