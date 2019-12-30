# https://www.dicionarioinformal.com.br/aparelho%20eletr%C3%B4nico/
# https://www.dicionarioinformal.com.br/ajax.php?funcao=autocomplete_def&query=ma

import json
import re
import sys
from urllib.error import HTTPError, URLError
# from urllib.request import urlopen as request
from urllib.parse import urlencode as encode, quote
from urllib.request import Request, urlopen

import unidecode
from bs4 import BeautifulSoup
from bs4 import element as bs4element

class Scrap:
    def __init__(self):
        self.base_url_dicio_informal = 'https://www.dicionarioinformal.com.br'
        self.ajax_url_dicio_informal = f'{self.base_url_dicio_informal}/ajax.php'
        self.base_url_sinonimos = 'https://www.sinonimos.com.br'
        self.base_url_dicio = 'https://www.dicio.com.br'

    def do_request(self, url):
        req = Request(url)
        req.add_header('Referer', url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        return urlopen(req).read()

    def format_url(self, url, path=None, query=None):
        formatted_url = url
        if path:
            formatted_url += f'{quote(path)}'
        if query:
            formatted_url += f'?{encode(query)}'
        return formatted_url

    def soup(self, url, path=None, query=None):
        url = self.format_url(url, path, query)
        content = self.do_request(url)
        soup = BeautifulSoup(content, 'html.parser')

        for script in soup(['script', 'style', 'link']):
            script.decompose()

        return soup

    def autocomplete(self, word):
        try:
            url = self.format_url(self.ajax_url_dicio_informal, query={'funcao': 'autocomplete_def', 'query': word})
            result = self.do_request(url).decode('latin-1') \
                .replace('\ ', ' ') \
                .replace('<em><span style=\\"color:#A9A9A9\\">', '') \
                .replace('</span><em>', '') \
                .replace('"', '') \
                .replace('\'', '"') \
                .replace('query', '"query"') \
                .replace('data', '"data"') \
                .replace('suggestions', '"suggestions"')
            result = json.loads(result)

            if result['suggestions']:
                del (result['suggestions'][-1])
                result['suggestions'] = list(map(lambda el: el.strip(), result['suggestions']))
                result['data'] = list(map(lambda el: el.strip(), result['data']))
                return list(zip(result['suggestions'], result['data']))
        except Exception as e:
            raise e

    def syn(self, word):
        word = unidecode.unidecode(word).lower().replace(' ', '-')
        soup = self.soup(self.base_url_sinonimos, f'/{word}')

        for script in soup(['script', 'style', 'link']):
            script.decompose()

        response = {'synonyms_meanings': [], 'synonyms': [], 'possible_synonyms': []}

        for item in soup.select('.s-wrapper'):
            text = item.text
            text = re.sub('\d', '', text).replace('.', '').split(': ')
            if len(text) == 1:
                text = text[0].strip().split(', ')
                response['synonyms'].append(text)
            else:
                meaning = text[0]
                synonyms = text[1].split(', ')
                if meaning.startswith('Principais sinônimos de '):
                    response['synonyms'].append(synonyms)
                else:
                    response['synonyms_meanings'].append({
                        'meaning': meaning,
                        'synonyms': list(map(lambda el: el.replace('Exemplo', ''), synonyms)),
                    })
        for item in soup.select('.possiveis-sinonimos'):
            response['possible_synonyms'].append(item.text.split(', '))
        return response

    def dictionary_informal(self, word):
        soup = self.soup(self.base_url_dicio_informal, path=f'/{word}')
        response = []
        for script in soup(['script', 'style', 'link']):
            script.decompose()
        for item in soup.find_all('p', class_='text-justify'):
            text = re.sub('\d\.\s', '', item.text)
            text = text.strip()
            response.append(text)
        return response

    def dictionary(self, word):
        word = unidecode.unidecode(word).replace(' ', '-').lower()
        soup = self.soup(self.base_url_dicio, path=f'/{word}')
        response = []
        content = soup.select('.significado')
        if len(content) >= 1:
            content = content[0]
            content.find_all('span')
            for item in content:
                if type(item) is bs4element.Tag and not item.get("class") and item.text:
                    response.append(item.text)
        return response

