import aioredis
from fastapi import FastAPI
from fastapi import status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from starlette.responses import Response

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


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
@cache(expire=86400)
async def home():
    return dict(message=f"Bem vindo a api ru uffs, acesse {app.docs_url} para mais informações")


@app.get("/campus/{campus}")
@cache(expire=86400)
async def ver_cardapio_campus(campus: str, response: Response):
    if campus == 'erechim':
        response.status_code = status.HTTP_302_FOUND
        return dict(message=f"Campus {campus} está em desenvolvimento.")
    bs = get_cardapio(campus)
    if not bs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return dict(message=f"Campus {campus} não encontrado.")
    cardapio = prepare_data(bs)
    response.status_code = status.HTTP_200_OK
    return {'cardapios': cardapio}


@app.get("/campus/{campus}/dia/{dia}")
@cache(expire=86400)
async def ver_cardapio_campus_dia(campus: str, dia: int, response: Response):
    bs = get_cardapio(campus)
    if not bs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return dict(message=f"Campus '{campus}' não encontrado.")

    cardapios = prepare_data(bs)
    if dia not in range(0, 5):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dict(message=f"Informe um dia entre 0 - 4.")
    cardapio = get_cardapio_dia(dia, cardapios)
    return dict(cardapios=cardapio)
