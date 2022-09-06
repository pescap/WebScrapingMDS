from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import json
from tqdm import tqdm
import sys
import time 
import pandas as pd



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



# Initiate the browser
browser  = webdriver.Chrome(ChromeDriverManager().install())

# Open the Website
browser.get('https://www.investing.com/')

# ========= Prealocacion Variables =========

precioFinal = 0
delta = 0
deltaPorcentual = 0


# ========= Buscar e ingresar a instrumento =========
# Ingresar a bucador
buscador = browser.find_element_by_xpath('//input[@placeholder="Search the website..."]')

try:
    buscador.click()
except:
    browser.find_element_by_xpath('//i[@class="popupCloseIcon largeBannerCloser"]').click()
    

# Se ingresa instrumento 
buscador.send_keys("Apple")
time.sleep(1.5)

# Se ingresa al primer resultado
buscador  = browser.find_element_by_xpath('//span[@class="second js-quote-item-symbol symbolName"]')
buscador.click()

# Se obtiene nemotecnico del instrumento
nemotecnico  = browser.find_element_by_xpath('//h2[@class="text-lg font-semibold"]').text.split()[0]


# Se obtiene delta del precio
delta = float(browser.find_element_by_xpath('//span[@data-test="instrument-price-change"]').text)

# ========= Data Historica =========

browser.find_element_by_link_text("Historical Data").click()

fecha = pd.to_datetime(browser.find_element_by_xpath('//td[@class="datatable_cell__3gwri font-bold"]').text)


precioFinal = float(browser.find_element_by_xpath('//td[@class="datatable_cell__3gwri datatable_cell--align-end__Wua8C datatable_cell--down__2CL8n"]').text)

volumen =  browser.find_element_by_xpath('//td[@data-test="volume-cell"]').text
volumen = float(volumen.replace("M", ""))

deltaPorcentual = browser.find_element_by_xpath('//td[@class="datatable_cell__3gwri datatable_cell--align-end__Wua8C datatable_cell--down__2CL8n font-bold"]').text
deltaPorcentual = deltaPorcentual[deltaPorcentual.find("(")+1:deltaPorcentual.rfind(")")]
deltaPorcentual = float(deltaPorcentual.replace("%", ""))


# ========= Articulos =========

# Se ingresa a seccion de noticias
browser.find_element_by_link_text("News & Analysis").click()

# Se obtiene url de noticias de articulo 
urlArticulos = browser.current_url #+ "/"

browser.close()

flag = True
# numPagina = 1

# while flag:
url = requests.get(urlArticulos,  headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(url.content, "html.parser")

primerArticulo =  soup.find("article", class_ = "js-article-item articleItem   ")

flag = False
















# titulosSelenium = browser.find_elements_by_xpath('//a[@class="title"]')
# titulos = [i.text for i in titulosSelenium]

# fechasSelenium = browser.find_elements_by_xpath('//span[@class="date"]')
# fechasArticulos = [i.text for i in fechasSelenium]

# Cada articulo por pagina
# articulos = browser.find_elements_by_xpath('//article[@class="js-article-item articleItem   "]')


# for articulo in articulos:
#     contienePro = len(articulo.find_elements_by_xpath('.//img[@class="pro-title-list-icon"]'))
    
#     if not contienePro:
#         a = articulo.find_element_by_xpath('//a[@class="title"]') #get_attribute('href')
#         # linkArticulo.click()
#         browser.implicitly_wait(10)
#         ActionChains(browser).move_to_element(a).click(a).perform()
      
        

diccionario = {"Nemotecnico": nemotecnico,
               "Fecha" : fecha,
               "Precio final": precioFinal,
               "Variacion en USD": delta,
               "Variacion Porcentual": deltaPorcentual,
               "Volumen (M)": volumen}


# //a[@class="title"]