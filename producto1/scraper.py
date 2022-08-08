from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xlrd
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import chromedriver_binary
import requests
from random import randint
import re
import os


URL = 'https://climatologia.meteochile.gob.cl/application/index/productos/RE2009'


# Se define la ruta de descarga
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "Descargas")
prefs = {"download.default_directory" : path}
chromeOptions.add_experimental_option("prefs",prefs)

# Estacion 330020 es quinta normal
estacion = '330020'
# Años a usar
años = list(range(1990, 2022))
# Estas dos lineas de codigo son si por x razon ChromeDriverManager tira error, se pone el path de manera manual
DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, chrome_options = chromeOptions)
driver.get(URL)

# Estas son las linea usadas normalmente
#driver = webdriver.Chrome(ChromeDriverManager.install())
#driver.get(URL)


for año in años:
    # Se envia la info a la pagina
    driver.find_elements_by_tag_name('input')[0].clear()
    driver.find_elements_by_tag_name('input')[0].send_keys(estacion)
    driver.find_elements_by_tag_name('input')[3].clear()
    driver.find_elements_by_tag_name('input')[3].send_keys(año)
    driver.find_element_by_class_name('btn-primary').click()

    # Se descargan los datos
    wait = WebDriverWait(driver, 10)
    boton_descarga = wait.until(EC.visibility_of_element_located((By.ID, 'btnExport')))
    boton_descarga.click()
    # Tiempo de descarga
    time.sleep(1)
    for file in os.listdir(path):
        if 'xls' in file: 
            df = pd.read_html(os.path.join(path, file))
            resumen_mensual = df[0].loc[33:33]
            print(resumen_mensual)
            df = df[0].loc[0:30]
            resumen_mensual.columns = resumen_mensual.columns.droplevel()
            resumen_mensual['Año'] = año
            df.columns = df.columns.droplevel()
            print(df.columns)
            df.to_excel('{}_{}.xlsx'.format(estacion,str(año)), index = False)
            resumen_mensual.to_excel('ResumenMensual_{}_{}.xlsx'.format(estacion, str(año)), index = False)
            os.remove(os.path.join(path, file)) 
    driver.back()

driver.close()
