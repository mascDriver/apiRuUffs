from fastapi import FastAPI
from webscraping.get_data import get_cardapio, prepare_data
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/campus/{campus}")
async def ver_cardapio(campus: str):
    bs = get_cardapio(campus)
    if not bs:
        return {"message": f"Campus {campus} não encontrado"}
    data = prepare_data(bs)
    return json.dumps({'cardapios': data})
