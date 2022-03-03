from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_cardapio(campus: str):
    html = urlopen(f"https://www.uffs.edu.br/campi/{campus}/restaurante_universitario")
    if html.code != 200:
        return False
    bs = BeautifulSoup(html, 'html.parser')
    return bs


def prepare_data(bs: BeautifulSoup):
    linhas = bs.find_all('section', {'id':'content-core'})
    conteudo_cardapios = linhas[0].findChildren('dl')
    cardapios = list()
    for conteudo_cardapio in conteudo_cardapios:
        cardapio_html = conteudo_cardapio.findChildren('tbody')[0].findChildren('td')
        cardapio = {
            'semana': linhas[0].findChildren('p')[11].text,
            'cardapio' : [
                {
                    'dia': cardapio_html[key].findChildren('p')[0].text if len(cardapio_html[key].findChildren('p')) == 1 else cardapio_html[key].text ,
                    'salada': cardapio_html[4+key].findChildren('p')[0].text if len(cardapio_html[4+key].findChildren('p')) == 1 else cardapio_html[4+key].text ,
                    'salada1': cardapio_html[9+key].findChildren('p')[0].text if len(cardapio_html[9+key].findChildren('p')) == 1 else cardapio_html[9+key].text ,
                    'salada2': cardapio_html[14+key].findChildren('p')[0].text if len(cardapio_html[14+key].findChildren('p')) == 1 else cardapio_html[14+key].text ,
                    'arroz': cardapio_html[19+key].findChildren('p')[0].text if len(cardapio_html[19+key].findChildren('p')) == 1 else cardapio_html[19+key].text ,
                    'arroz1': cardapio_html[24+key].findChildren('p')[0].text if len(cardapio_html[24+key].findChildren('p')) == 1 else cardapio_html[24+key].text ,
                    'feijao': cardapio_html[29+key].findChildren('p')[0].text if len(cardapio_html[29+key].findChildren('p')) == 1 else cardapio_html[29+key].text ,
                    'acompanhamento': cardapio_html[34+key].findChildren('p')[0].text if len(cardapio_html[24+key].findChildren('p')) == 1 else cardapio_html[34+key].text ,
                    'mistura': cardapio_html[39+key].findChildren('p')[0].text if len(cardapio_html[39+key].findChildren('p')) == 1 else cardapio_html[39+key].text ,
                    'mistura_vegana': cardapio_html[44+key].findChildren('p')[0].text if len(cardapio_html[44+key].findChildren('p')) == 1 else cardapio_html[44+key].text ,
                    'sobremesa': cardapio_html[49+key].findChildren('p')[0].text if len(cardapio_html[49+key].findChildren('p')) == 1 else cardapio_html[49+key].text ,
                }for key in range(0, 5)
            ]
        }
        cardapios.append(cardapio)
    return cardapios

