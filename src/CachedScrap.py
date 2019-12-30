from datetime import datetime
import pickle
from os import path
from Scrap import Scrap


class CachedScrap:
    def __init__(self, cache_path='./.cache'):
        self.cache_path = cache_path
        self.scrap = Scrap()
        self.create_dir()

    def get_data(self, method, word):
        data = self.seek_cache(method, word)
        if data:
            return data['data']
        else:
            if method == 'syn':
                data = self.scrap.syn(word)
            elif method == 'dictionary_informal':
                data = self.scrap.dictionary_informal(word)
            elif method == 'dictionary':
                data = self.scrap.dictionary(word)
            elif method == 'autocomplete':
                data = self.scrap.autocomplete(word)

            self.save_cache(method, word, data)
            return data

    def syn(self, word):
        return self.get_data('syn', word)

    def dictionary_informal(self, word):
        return self.get_data('dictionary_informal', word)

    def dictionary(self, word):
        return self.get_data('dictionary', word)

    def autocomplete(self, word):
        return self.get_data('autocomplete', word)

    def file_name(self, method, word):
        return f'{method}.{word}.cache'

    def seek_cache(self, method, word):
        filename = self.file_name(method, word)
        if self.has_file(filename):
            file = open(self.cache_path + '/' + filename, 'rb')
            data = pickle.load(file)
            file.close()
            return data

    def save_cache(self, method, word, data):
        filename = self.file_name(method, word)
        file = open(self.cache_path + '/' + filename, 'wb')
        pickle.dump(
            {
                'data': data,
                'cacheDate': datetime.now().timestamp()},
            file)
        file.close()

    def create_dir(self):
        import os
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def has_file(self, name):
        return path.exists(self.cache_path + '/' + name) and path.isfile(self.cache_path + '/' + name)
