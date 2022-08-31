# Tratamiento de datos
# ==============================================================================
import numpy as np
import pandas as pd
from tabulate import tabulate
import re
import time


# Manejo Web, paginas y webScrapping
# ==============================================================================
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs


# Gráficos
# ==============================================================================
from matplotlib import pyplot as plt


# Configuración warnings
# ==============================================================================\n",
import warnings
warnings.filterwarnings('ignore')

# Funciones 
def LoginLinkedin(usuario, clave,edgeBrowser):
    # locate email form by_class_name
    username = edgeBrowser.find_element(By.ID,value='session_key')
    # send_keys() to simulate key strokes
    username.send_keys(usuario)
    # locate password form by_class_name
    password = edgeBrowser.find_element(By.ID,value='session_password')
    # send_keys() to simulate key strokes
    password.send_keys(clave)
    # locate submit button by_class_name
    log_in_button = edgeBrowser.find_element(By.CLASS_NAME, 'sign-in-form__submit-button')
    # .click() to mimic button click
    log_in_button.click()

    
def leerUrl(pagina):    
    soup = bs(urllib.request.urlopen(pagina).read().decode())
    return  soup
    
def ExtraerLink(linkPage,patron):
    lista = []
    for tag in linkPage:
        valor = tag.get('href')
        if(str(valor).find(patron) != -1):
            lista.append(valor)
    df = pd.DataFrame (lista, columns = ['url'])
    df = df.drop_duplicates()
    return df


# Instantiate the webdriver with the executable location of MS Edge
# Provide the full location of the path to recognise correctly
PATH = 'App\msedgedriver.exe'
edgeBrowser = webdriver.Edge(PATH)

# This is the step for maximizing browser window
edgeBrowser.maximize_window()

# Browser will get navigated to the given URL
edgeBrowser.get('https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Chile&locationId=&geoId=104621616&f_TPR=r86400&position=1&pageNum=0')

time.sleep(3)

linkedin_soup = bs(edgeBrowser.page_source.encode("utf-8"), "html")
linkedin_soup.prettify()

patron = '/jobs/view/'
df = ExtraerLink(linkedin_soup('a'),patron)
df.to_parquet('output/linkdb.parquet')
