from flask import Flask, jsonify
from Scrap import Scrap
from CachedScrap import CachedScrap

def server(port=5000):
    app = Flask(__name__)
    #scrap = Scrap()
    scrap = CachedScrap()

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route("/synonyms/<word>")
    def synonyms(word):
        return jsonify(scrap.syn(word))

    @app.route("/autocomplete/<word>")
    def autocomplete(word):
        return jsonify(scrap.autocomplete(word))

    @app.route("/informal-dictionary/<word>")
    def informal_dictionary(word):
        return jsonify(scrap.dictionary_informal(word))

    @app.route("/dictionary/<word>")
    def dictionary(word):
        return jsonify(scrap.dictionary(word))

    app.run(host='127.0.0.1', port=port, debug=True)

