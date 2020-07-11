


if __name__ == "__main__":

    import pandas as pd
    from selenium import webdriver
    from obras_bot import ObrasBot
    
    #configuração do bot
    nome_csv = 'audiovisual_bot.csv'
    browser = webdriver.Chrome(r"C:\Users\<--usuario-->\Downloads\chromedriver_win32\chromedriver.exe")
    portal_url = "http://portal.mj.gov.br/ClassificacaoIndicativa/jsps/ConsultarObraForm.do?inicio_action"
    categorias = ["longa metragem"] #verifique as categorias(curta metragem, longa metragem e etc) disponíveis no site
    veiculo = ["cinema"] #verifique os veículos(cinema, televisão e etc) disponíveis no site

    #inicialização do bot
    bot = ObrasBot(browser, portal_url, categorias, veiculo, nome_csv,
                   "OBRA", "DIRETOR", "VEICULO", "DISTRIBUIDOR", "CLASSIFICACAO") #colunas que a base terá
    bot.criaBase() #cria um csv vazio que será preenchido posteriormente
    
    #coleta dos dados no site
    titulo_obra = pd.read_excel("obras_audiovisual.xlsx") #amostra com uma coluna apenas contendo o nome das obras
    titulo_obra = sorted(set(list(titulo_obra['TÍTULO.ORIGINAL']))) #elimina os nomes repetidos
    for obra in titulo_obra:
        bot.portalObras(obra)
    bot.limpaBase() #remove linhas repetidas(ocorre pela maneira como o site exibe as informações)
