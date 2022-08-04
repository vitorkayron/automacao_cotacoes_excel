from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

navegador = webdriver.Chrome()

# Passo 1: Pegar cotação do dólar

# entrar no site do google
navegador.get("https://www.google.com/")

# pesquisar cotação dólar
navegador.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
navegador.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar cotação na página do google
cotacao_dolar = navegador.find_element("xpath", '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

# Passo 2: Pegar cotação do euro

# entrar no site do google
navegador.get("https://www.google.com/")

# pesquisar cotação euro
navegador.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar cotação da página no google
cotacao_euro = navegador.find_element("xpath", '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")


# Passo 3: Pegar cotação do ouro

# entrar no site
navegador.get("https://www.melhorcambio.com/ouro-hoje")

#pegar cotação no site
cotacao_ouro = navegador.find_element("xpath", '//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(',', '.')

# Passo 4: Importar a base de dados
tabela = pd.read_excel("Produtos.xlsx")

# Passo 5: Atualizar cotação, preço de compra e preço de venda

#atualizar cotação
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

#atualizar preço de compra = preço original  * cotação
tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]


#atualizar preço de venda = preço de compra * margem de lucro
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

# Passo 6: Exportar o relatório atualizado
tabela.to_excel("Produtos Novo.xlsx", index=False)
navegador.quit()

