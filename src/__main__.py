
from TUI import Tui
from Server import server

if __name__ == '__main__':
    import sys

    try:
        if len(sys.argv) > 1:
            print('Running on server mode')
            if sys.argv[1]  == '--server' or sys.argv[1] == '-s': 
                if len(sys.argv) == 3:
                    print(f'Using port {sys.argv[2]}')
                    server( int( sys.argv[2] ) )
                else: 
                    print('Using default port')
                    server( )
            else:
                Tui().look_for( sys.argv[1] )
        else:
            tui = Tui()
            tui.separate()
            print('\n'
                  'O SYN é uma ferramenta de busca de sinônimos, significados e termos similares em português.\n'
                  'Foi escrito em Python e utiliza "web scrapping", ou seja, os resultados daqui são extraídos de'
                  'paginas web como sinonimos.com.br, dicio.com.br e dicionarioinformal.com.br, assim, os resultados'
                  'podem não estar formatados perfeitamente e dependem da formatação destes sites no momento'
                  'em que a ferramenta foi escrita.\n'
                  '\n'
                  'As pesquisas realizadas serão armazenadas em arquivos de cache para aumentar a velocidade em '
                  'pesquisas posteriores. Serão armazenados no diretório de execução da ferramenta, em .cache.'
                  '\n'
                  '* Utilize --server para iniciar a aplicação no modo servidor (uma API será iniciada na sua máquina, '
                  'e os resultados serão retornados no formato JSON);\n'
                  '\n'
                  '* Use o termo de pesquisa como parâmetro para pesquisar um termo apenas;\n'
                  '\n'
                  '* Execute sem nenhum parâmetro para iniciar o modo interativo, utilize CTRL + C para sair.\n')
            tui.separate()

            while True:
                word = str(input('palavra > '))
                tui.look_for(word)
    
    except KeyboardInterrupt:
        print('')