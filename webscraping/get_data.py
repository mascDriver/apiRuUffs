from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

def get_value_by_position(lista: list, position: int):
    try:
        return lista[position].text.replace('\n', '').strip()
    except IndexError:
        return ''

def get_cardapio(campus: str):
    try:
        if campus == 'realeza':
            html = urlopen(f"https://www.uffs.edu.br/campi/{campus}/restaurante_universitario/apresentacao-do-ru")
        else:
            html = urlopen(f"https://www.uffs.edu.br/campi/{campus}/restaurante_universitario")
    except HTTPError:
        return False
    if html.code != 200:
        return False
    return BeautifulSoup(html, 'html.parser')


def prepare_data(bs: BeautifulSoup):
    linhas = bs.find_all('section', {'id':'content-core'})
    conteudo_cardapios = linhas[0].findChildren('table') or linhas
    cardapios = list()
    for conteudo_cardapio in conteudo_cardapios:
        cardapio_html = conteudo_cardapio.findChildren('td')
        cardapio = {
            'semana': conteudo_cardapio.find_previous('p').text,
            'cardapio' : [
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
                }for key in range(0, 5)
            ]
        }
        cardapios.append(cardapio)
    return cardapios

def get_cardapio_dia(dia: int, cardapios: list):
    return list(map(lambda x: x['cardapio'][dia], cardapios))