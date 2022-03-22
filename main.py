from fastapi import FastAPI, Response, status
from webscraping.get_data import get_cardapio, prepare_data, get_cardapio_dia

app = FastAPI(
    title='Api R.U UFFS',
    version='0.0.1',
    contact={
        "name": "Diogo Baltazar do Nascimento",
        "url": "https://github.com/mascDriver",
        "email": "diogobaltazardonascimento@outlook.com",
    },
)


@app.get("/")
async def home():
    return {"message": f"Bem vindo a api ru uffs, acesse {app.docs_url} para mais informações"}


@app.get("/campus/{campus}")
async def ver_cardapio_campus(campus: str, response: Response):
    if campus == 'erechim':
        response.status_code = status.HTTP_302_FOUND
        return {"message": f"Campus {campus} está em desenvolvimento."}
    bs = get_cardapio(campus)
    if not bs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Campus {campus} não encontrado."}
    cardapio = prepare_data(bs)
    response.status_code = status.HTTP_200_OK
    return {'cardapios': cardapio}

@app.get("/campus/{campus}/dia/{dia}")
async def ver_cardapio_campus_dia(campus: str, dia: int, response: Response):
    bs = get_cardapio(campus)
    if not bs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Campus '{campus}' não encontrado."}
    cardapios = prepare_data(bs)
    if dia not in range(0,5):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Informe um dia entre 0 - 4."}
    cardapio = get_cardapio_dia(dia, cardapios)
    return {'cardapios': cardapio}
