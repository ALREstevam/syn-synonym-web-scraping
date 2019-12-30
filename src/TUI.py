import json
import re
from pprint import pprint
from urllib.error import HTTPError, URLError
from colorama import Fore as T, Back as B, Style as S, init as init_colorama
from tabulate import tabulate
from CachedScrap import CachedScrap
import copy
import os

init_colorama()
RESET = S.RESET_ALL
BOLD = S.BRIGHT

EMPTY_SEARCH = 'Não foi informado nenhum termo de pesquisa'


#def chunk(it, size):
#    from itertools import islice
#    it = iter(it)
#    return iter(lambda: tuple(islice(it, size)), ())

#def terminal_size():
#    try:
#        import curses
#        w = curses.initscr()
#        height, width = w.getmaxyx()
#        return {'rows': height, 'cols': width}
#    except:
#        return {'rows': 25, 'cols': 80}


class Tui:
    def __init__(self):
        self.scrap = CachedScrap()
        # self.scrap = Scrap()

    def print_until_len(self, list, max_len=30, bullet_color=T.GREEN):
        printed_len = 0
        for item in list:
            item = item.strip()
            item = re.sub(r'\n+', '\n', item)
            item = item.replace('\n', ' · ')
            print(f'{BOLD}{bullet_color}•{RESET} {item}')
            printed_len += len(item)
            if printed_len > max_len:
                return printed_len
        return printed_len

    def print_topics(self, list, bullet_color=T.GREEN):
        for item in list:
            print(f'{BOLD}{bullet_color}•{RESET} {item}')

    def print_panels(self, data, bullet_color=T.GREEN, title_color=T.RED):
        chunks = []
        panels = {}

        for index, item in enumerate(data):
            title = f'{title_color}{item["meaning"]}{RESET}'
            panel = list(map(lambda el: f'{BOLD}{bullet_color}•{RESET} {el}', item['synonyms']))
            panels[title] = panel

            if (index + 1) % 3 == 0 or index == len(data)-1:
                chunks.append(copy.deepcopy(panels))
                panels = {}

        for chunk_item in chunks:
            print()
            print(tabulate(chunk_item, headers='keys', tablefmt='plain'))

    def separate(self):
        #ts = terminal_size()
        #print(f'\n{"#" * ts["cols"]}\n')
        print('\n\n')
        print(85 * '#')


    def look_for(self, word):

        if word == "":
            print(EMPTY_SEARCH)
            return

        print(f'{BOLD}{B.BLACK}{T.GREEN}┌{50 * "─"}┐{RESET}')
        print(f'{BOLD}{B.BLACK}{T.GREEN}│{word.upper():^50s}│{RESET}')
        print(f'{BOLD}{B.BLACK}{T.GREEN}└{50 * "─"}┘{RESET}')
        print()

        dictionary = None

        try:
            dictionary = self.scrap.dictionary(word)
            printed_len = 0
            if dictionary:
                print(f'{T.LIGHTGREEN_EX}{BOLD}[ SIGNIFICADOS ]{RESET}')
                printed_len = self.print_until_len(dictionary, 500, T.LIGHTGREEN_EX)
        except (HTTPError) as e:
            print('\n[ Nenhum significado encontrado no dicionário :( ]')
        except URLError as e:
            print(f'\n{T.RED}{BOLD}/!\\ ERROR WHILE REQUESTING SYNONYMS  {RESET}{T.RED}: {e}{RESET}\n')

        try:
            print()
            autocomplete = self.scrap.autocomplete(word)

            if autocomplete:
                print(f'{T.LIGHTYELLOW_EX}{BOLD}[ SIMILARES ]{RESET}')
                self.print_topics(list(map(lambda el: f'{T.LIGHTYELLOW_EX}{el[0].upper()}{RESET}: {el[1]}', autocomplete)), T.YELLOW)
            else:
                print('\n[ Nenhum termo similar encontrado :( ]')
        except (HTTPError) as e:
                print('\n[ Nenhum termo similar encontrado :( ]')
        except URLError as e:
            print(f'\n{T.RED}{BOLD}/!\\ ERROR WHILE REQUESTING SYNONYMS  {RESET}{T.RED}: {e}{RESET}\n')
        except json.decoder.JSONDecodeError as e:
            print(f'\n{T.RED}{BOLD}⚠️ erro ao decodificar JSON{RESET}{T.RED}: {e}{RESET}\n')

        try:
            if not dictionary or printed_len < 300:
                informal = self.scrap.dictionary_informal(word)
                if informal:
                    print()
                    print(f'{T.LIGHTMAGENTA_EX}{BOLD}[ SIGNIFICADOS INFORMAIS ]{RESET}')
                    self.print_until_len(informal, 400, T.LIGHTMAGENTA_EX)
                else:
                    print('\n[ Nenhum significado informal encontrado :( ]')
        except (HTTPError) as e:
            print('\n[ Nenhum significado informal encontrado :( ]')
        except URLError as e:
            print(f'\n{T.RED}{BOLD}/!\\ ERROR WHILE REQUESTING SYNONYMS  {RESET}{T.RED}: {e}{RESET}\n')

        try:
            syns = self.scrap.syn(word)
            if syns:
                print()
                print(f'{T.LIGHTRED_EX}{BOLD}[ SINÔNIMOS ]{RESET}')

                self.print_panels(syns['synonyms_meanings'], bullet_color=T.LIGHTRED_EX)

                if syns['synonyms']:
                    print()
                    print(f'{T.LIGHTRED_EX}Outros sinônimos{RESET}')
                    for other_syn in syns['synonyms']:
                        self.print_topics(other_syn, T.LIGHTRED_EX)

                if syns['possible_synonyms']:
                    print()
                    print(f'{T.LIGHTRED_EX}Similares{RESET}')
                    for possible in syns['possible_synonyms']:
                        self.print_topics(possible, T.LIGHTRED_EX)
            print()

        except (HTTPError) as e:
            print('\n[ Nenhum sinônimo encontrado :( ]')
        except URLError as e:
            print(f'\n{T.RED}{BOLD}/!\\ ERROR WHILE REQUESTING SYNONYMS  {RESET}{T.RED}: {e}{RESET}\n')
        finally:
            self.separate()
            print(RESET)

