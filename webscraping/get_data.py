from requests_html import HTML, HTMLSession
from urllib.error import HTTPError
from unicodedata import normalize
from requests.exceptions import ChunkedEncodingError
from websockets.exceptions import ConnectionClosed


def get_value_by_position(lista: list, position: int):
    try:
        return lista[position].text.replace('\n', '').strip()
    except IndexError:
        return ''


def normalize_url(url: str):
    return normalize('NFKD', url).encode('ASCII','ignore').decode('ASCII').lower().replace(' ', '-')


def get_cardapio(campus: str):
    try:
        if campus == 'realeza':
            url = f"https://www.uffs.edu.br/campi/{normalize_url(campus)}/restaurante_universitario/apresentacao-do-ru"
        elif campus == 'passo-fundo':
            url = f"https://www.uffs.edu.br/campi/{normalize_url(campus)}/restaurante-universitario"
        else:
            url = f"https://www.uffs.edu.br/campi/{normalize_url(campus)}/restaurante_universitario"

        session = HTMLSession()
        response = session.get(url, allow_redirects=False)

    except HTTPError:
        return False
    except ChunkedEncodingError:
        return False
    except ConnectionClosed:
        return False

    if response.status_code != 200:
        return False

    session.close()
    return response.html


def prepare_data(html: HTML):
    conteudo_cardapios = html.find('table') or html.find('#content-core', first=True)
    semanas = iter(html.find('#content-core p', containing='Semana ')[::-1])
    cardapios = list()

    for conteudo_cardapio in conteudo_cardapios:
        cardapio_html = conteudo_cardapio.find('td')

        cardapio = {
            'semana': next(semanas).text,
            'cardapio': [
                {
                    'dia': get_value_by_position(cardapio_html, key),
                    'salada': get_value_by_position(cardapio_html, 5+key),
                    'salada1': get_value_by_position(cardapio_html, 10+key),
                    'salada2': get_value_by_position(cardapio_html, 15+key),
                    'graos': get_value_by_position(cardapio_html, 20+key),
                    'graos1': get_value_by_position(cardapio_html, 25+key),
                    'graos2': get_value_by_position(cardapio_html, 30+key),
                    'acompanhamento': get_value_by_position(cardapio_html, 35+key),
                    'mistura': get_value_by_position(cardapio_html, 40+key),
                    'mistura_vegana': get_value_by_position(cardapio_html, 45+key),
                    'sobremesa': get_value_by_position(cardapio_html, 50+key),
                } for key in range(0, 5)
            ]
        }
        cardapios.append(cardapio)
    return cardapios


def get_cardapio_dia(dia: int, cardapios: list):
    return list(map(lambda x: x['cardapio'][dia], cardapios))
