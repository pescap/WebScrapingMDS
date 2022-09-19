# Scraper portalinmobiliario.com

import os
import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import random
from datetime import datetime

# Función para espera aleatoria

def espera():
    tiempo = round(random.uniform(1, 3), 1)
    sleep(tiempo)
    return

# Configuraciones estandar para poder ejecutar el navegador web

chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output\\")
prefs = {"download.default_directory" : path, "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs",prefs)

# URL del sitio web desde el que se extraerá la información

URL = 'https://www.portalinmobiliario.com/arriendo/departamento/vina-del-mar-valparaiso'

# Abrir el navegador e ingresar a la URL de Interés

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)
espera()

driver.find_element(By.XPATH,"/html/body/div[2]/div/button").click()

### Ingreso de parámetros (filtros)

## Selección de los barrios de interés

# Barrio 1

driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section/div[5]/ul/li[2]/a/span[1]').click()
espera()

# Barrio 2

driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[4]/ul/li[8]/a/span[1]').click()
espera()

# Barrio 3

driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[4]/ul/li[7]/a/span[1]').click()
espera()

## Variables de String a utilizar

precio_max = 700000  # máximo 700.000 CLP
piezas = 2  # mínimo 2 habitaciones

# Ingresar precio máximo de arriendo

input_precio_max = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[5]/ul/li[5]/form/div[2]/div/label/div/input')
input_precio_max.send_keys(precio_max)
input_precio_max.send_keys(Keys.ENTER)
espera()

# Ingresar cantidad mínima de habitaciones

input_piezas = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[8]/ul/li[5]/form/div[1]/div/label/div/input')
input_piezas.send_keys(piezas)
input_piezas.send_keys(Keys.ENTER)
espera()


# Ordenamiento por precio

ordenar_resultados = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/section/div[1]/div/div/div[2]/div[2]').click()
espera()

driver.find_element(By.XPATH ,'//*[@id="andes-dropdown-más-relevantes-list-option-price_asc"]').click()
espera()

# Dataframe para almacenamiento de resultados

columnas = ['fecha-hora', 'link', 'id_publicacion', 'descripcion', 'precio', 'habitaciones', 'superficie']
df_props = pd.DataFrame(columns=columnas)

# Paso de contenedor de propiedades mostradas a Beautiful Soup

import requests
resultados = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/section')
cod_results = resultados.get_attribute('innerHTML')

#url ="https://www.portalinmobiliario.com/arriendo/departamento/valparaiso/vina-del-mar/libertad-o-recreo-o-miraflores/_OrderId_PRICE_PriceRange_0CLP-700000CLP_BEDROOMS_2-*_NoIndex_True"

#cod_results = requests.get(url)

soup = BeautifulSoup(cod_results, 'html.parser')


lista = soup.find_all('a', class_="ui-search-result__content-wrapper ui-search-link")

# Recorrido de todas las propiedades

hoy = datetime.today().strftime('%F')

for link in lista:
    try:
        linea = pd.DataFrame(columns=columnas)
        
        # Obtención link de la propiedad
        
        link_prop = link.get('href')

        # Apertura de browser con propiedad

        driver.get(link_prop)
        espera()

        # Obtención y registro de datos en dataframe
        
        linea.loc[0, 'fecha-hora'] = hoy   

        linea.loc[0, 'link'] = link_prop

        elem_codigo = driver.find_element(By.XPATH, '//*[@id="denounce"]/div/p/span')
        codigo = elem_codigo.text
        linea.loc[0, 'id_publicacion'] = codigo

        elem_descripcion = driver.find_element(By.XPATH, '//*[@id="description"]/div/p')
        descripcion = elem_descripcion.text
        linea.loc[0, 'descripcion'] = descripcion

        elem_precio = driver.find_element(By.XPATH, '//*[@id="price"]/div/div/span/span[3]')
        precio = elem_precio.text
        linea.loc[0, 'precio'] = precio

        elem_habitaciones = driver.find_element(By.XPATH, '//*[@id="technical_specifications"]/div/div[1]/table/tbody/tr[4]/td/span')
        habitaciones = elem_habitaciones.text
        linea.loc[0, 'habitaciones'] = habitaciones

        elem_superficie = driver.find_element(By.XPATH, '//*[@id="technical_specifications"]/div/div[1]/table/tbody/tr[1]/td/span')
        superficie = elem_superficie.text
        linea.loc[0, 'superficie'] = superficie

        df_props = pd.concat([df_props, linea], ignore_index=True)
        print('Ok', end=' ')
        espera()
        
    except:
        print('Abortado', end=' ')
        espera()
        
        
df_props["precio1"] = df_props["precio"].str.extract("(\d*\.?\d+)", expand=True)

df_props["superficie1"] = df_props['superficie'].str.split(' ').apply(lambda x: float(x[0]))

df_props["habitaciones"] = df_props["habitaciones"].astype(int)

import plotly.express as px

fig = px.scatter(df_props, x="precio1", y="superficie1",color='habitaciones',
                labels={
                     "precio1": "Precio (CLP)",
                     "superficie1": "Superficie (m2)",
                     "habitaciones": "# de Habitaciones"
                 },
                title="Superficie v/s Precio")
fig.show()

#Guardamos el gráfico para abrirlo en Readme

fig.write_image("grafico.png")

#Guardamos el DataFrame en un archivo .csv diariamente

df_props.to_csv(f'output_{datetime.today().strftime("%d-%m-%Y")}.csv')
