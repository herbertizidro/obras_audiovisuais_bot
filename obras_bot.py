

if __name__ != "__main__":

    import csv
    import time
    import pandas as pd


    class ObrasBot():
        def __init__(self, browser, portal_url, categorias, veiculo, nome_csv, *colunas):
            self.browser = browser
            self.categorias = [c.upper() for c in categorias]
            self.veiculo = [v.upper() for v in veiculo]
            self.portal_url = portal_url
            self.nome_csv = nome_csv
            self.colunas = list(colunas)

            #acessa o site
            self.browser.get(self.portal_url)
            self.browser.maximize_window()

            #botao busca avancada
            self.browser.find_element_by_xpath(
                "/html/body/table/tbody/tr/td/table[6]/tbody/tr/td/form[1]/table[1]/tbody/tr[3]/td/a"
            ).click()
            time.sleep(2)


        def criaBase(self):
            with open(self.nome_csv, 'w') as base:
                writer = csv.DictWriter(base, self.colunas)
                writer.writeheader()

        def alimentaBase(self, obra, diretores, veiculo, distribuidor, classificacao):
            with open(self.nome_csv, 'a') as base:
                writer = csv.DictWriter(base, self.colunas)
                writer.writerow({self.colunas[0]: obra,
                                 self.colunas[1]: diretores,
                                 self.colunas[2]: veiculo,
                                 self.colunas[3]: distribuidor,
                                 self.colunas[4]: classificacao})

        def limpaBase(self):
            base = pd.read_csv(self.nome_csv, encoding='ISO-8859-1') #ou latin 1
            base.drop_duplicates(inplace=True)
            base.to_csv(self.nome_csv, index=False, encoding='ISO-8859-1')
            self.browser.quit()

        def portalObras(self, obra):
            obra = obra.upper().replace('"', '')
            #limpa o campo
            self.browser.find_element_by_xpath(
                "/html/body/table/tbody/tr/td/table[6]/tbody/tr/td/form[1]/table[1]/tbody/tr[1]/td[2]/input").clear()
            #digita o titulo
            titulo_br_input = self.browser.find_element_by_xpath(
                "/html/body/table/tbody/tr/td/table[6]/tbody/tr/td/form[1]/table[1]/tbody/tr[1]/td[2]/input")
            for o in obra:
                time.sleep(0.1)
                titulo_br_input.send_keys(o)
            #botao consultar
            self.browser.find_element_by_xpath(
                "/html/body/table/tbody/tr/td/table[6]/tbody/tr/td/form[1]/table[2]/tbody/tr/td/a"
            ).click()
            time.sleep(2)            
            linha = 1            
            while True:                
                try:                
                    #pega o titulo br e categoria presentes na tabela 1
                    titulo_br_tabela = self.browser.find_element_by_xpath(
                        '//*[@id="lista"]/tbody/tr[' + str(linha) + ']/td[1]'
                    ).text                    
                    categoria_tabela = self.browser.find_element_by_xpath(
                        '//*[@id="lista"]/tbody/tr[' + str(linha) + ']/td[4]'
                    ).text                    
                    if titulo_br_tabela.strip().upper() == obra and categoria_tabela.strip().upper() in self.categorias:
                        #abre a página de interesse clicando num botão presente em cada linha da tabela 1
                        self.browser.find_element_by_xpath('//*[@id="lista"]/tbody/tr[' + str(linha) + ']/td[5]/a').click()
                        time.sleep(2)
                        aux = 1
                        while True:
                            try:
                               #acessa a tabela 2, filtra os diretores e novamente a categoria
                                categoria_tabela2 = self.browser.find_element_by_xpath(
                                    '//*[@id="TRbl_report_ClassificacaoProcessoObraView'+str(aux)+'"]/td[4]'
                                ).text
                                veiculo_tabela2 = self.browser.find_element_by_xpath(
                                    '//*[@id="TRbl_report_ClassificacaoProcessoObraView'+str(aux)+'"]/td[3]'
                                ).text                                
                                if categoria_tabela2.strip().upper() in self.categorias and veiculo_tabela2.strip().upper() in self.veiculo:
                                    diretores_tabela = self.browser.find_element_by_xpath(
                                        '//*[@id="TRbl_report_TbObra"]/tbody/tr[6]/td'
                                    ).text
                                    #quando é mais de um diretor(a)
                                    #costuma vir assim: Jurandir Muller/Roberto Tibiriçá/Claudia Priscilla
                                    diretores_tabela = diretores_tabela.replace('Diretores:', '').replace('/', ' - ').replace('"', '').strip().upper()
                                    veiculo = self.browser.find_element_by_xpath('//*[@id="TRbl_report_ClassificacaoProcessoObraView'+str(aux)+'"]/td[3]').text
                                    distribuidor = self.browser.find_element_by_xpath('//*[@id="TRbl_report_ClassificacaoProcessoObraView'+str(aux)+'"]/td[5]').text
                                    distribuidor = distribuidor.replace('"', "")
                                    classificacao = self.browser.find_element_by_xpath('//*[@id="TRbl_report_ClassificacaoProcessoObraView'+str(aux)+'"]/td[6]').text
                                    self.alimentaBase(obra, diretores_tabela, veiculo, distribuidor, classificacao)                                    
                                aux += 1
                            except:
                                break
                        #voltar à página anterior
                        self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td/table[6]/tbody/tr/td/a').click()
                    linha += 1                
                except:
                    break        

