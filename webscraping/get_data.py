import os
from unicodedata import normalize
import re
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
proxies = {
    "http://": f'http://'
               f'{os.environ.get("PROXY_USERNAME")}:'
               f'{os.environ.get("PROXY_PASSWORD")}@'
               f'{os.environ.get("PROXY_IP")}:'
               f'{os.environ.get("PROXY_PORT")}'
}


def get_value_by_position(lista: list, position: int):
    try:
        return lista[position].text.replace('\n', '').strip()
    except IndexError:
        return ''


def normalize_url(url: str):
    return normalize('NFKD', url).encode('ASCII', 'ignore').decode('ASCII').lower().replace(' ', '-')


def get_cardapio(campus: str):
    try:
        if campus == 'realeza':
            html = httpx.get(f"https://uffs.edu.br/uffs/restaurantes-universitarios/campus-{normalize_url(campus)}#texto")
        else:
            html = httpx.get(f"https://uffs.edu.br/uffs/restaurantes-universitarios/campus-{normalize_url(campus)}#texto")
    except httpx.HTTPError:
        try:
            if campus == 'realeza':
                html = httpx.get(
                    f"https://uffs.edu.br/uffs/restaurantes-universitarios/campus-{normalize_url(campus)}#texto",
                    proxies=proxies)
            else:
                html = httpx.get(f"https://uffs.edu.br/uffs/restaurantes-universitarios/campus-{normalize_url(campus)}#texto",
                                 proxies=proxies)
        except httpx.HTTPError:
            return False
    if html.status_code != 200:
        return False
    return BeautifulSoup(html.text, 'html.parser')


def prepare_data(bs: BeautifulSoup):
    linhas = bs.find_all('div', {'id': 'cardapioCarousel'})
    conteudo_cardapios = linhas[0].find_all('div', {'class': 'carousel-item'})
    cardapio = {
        'semana': bs.find('div', {'class': 'cardapio-header'}).text,
        'cardapio': []
    }
    for x, conteudo_cardapio in enumerate(conteudo_cardapios):
        _, day, _, almoco, _, jantar = conteudo_cardapio.find_all(string=True)

        itens = re.split(r'[\/\n]+| {2,}', almoco.replace('c/', 'com'))

        # Remover espaços extras e itens vazios
        itens = [item.strip() for item in itens if item.strip()]
        data = {
                    'dia': day,
                    'salada': '',
                    'salada1': '',
                    'salada2': '',
                    'graos': '',
                    'graos1': '',
                    'graos2': '',
                    'acompanhamento': '',
                    'mistura': '',
                    'mistura_vegana': '',
                    'sobremesa': '',
                }
        for key, value in enumerate(data.keys()):
            if value == 'dia':
                continue
            data[value] = itens[key-1]
        cardapio['cardapio'].append(data)
    return cardapio


def get_cardapio_dia(dia: int, cardapios: list):
    return cardapios['cardapio'][dia]
