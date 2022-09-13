#!/usr/bin/env python
# coding: utf-8


# Importamos la librerias
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
import pandas as pd
import re

# Importamos Selenium
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os


# Copiamos la url del periodico BIO BIO
URL=requests.get("https://www.biobiochile.cl/lista/busca-2020/categorias/nacional")
soup=BeautifulSoup(URL.text,'html.parser')


# Creamos una variable que contengo los resultados de busqueda con beautiful soup
Titulares_Nacionales = soup.find("div", {"class": "results-container"})
Titulares_Nacionales


# Buscamos lo que hay en cada artículo de noticia
Articulos = Titulares_Nacionales.find_all('article',{'class':'article article-horizontal article-with-square justify-content-between'})
Articulos


# Creamos el driver para utilizar selenium y poder extraer el número de visitas
s = Service("C:\\Users\\ignac\\Downloads\\chromedriver.exe")
driver = webdriver.Chrome(service=s)


# Creamos un ciclo for para extraer la variables que queremos. Utilizamos Beautiful Soup y Selenium
d = []
for articulo in range(len(Articulos)):
    try:
        headline = Articulos[articulo].find('h2',{'class':"article-title"}).get_text().replace('"',"")
        Autor = Articulos[articulo].find('a',{'class':'article-author'}).get_text()
        Fecha = Articulos[articulo].find('div',{'class':'article-date-hour'}).get_text().strip()
        Link  = Articulos[articulo].find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+'))['href']
        driver = webdriver.Chrome(service=s)
        driver.get(Link)
        visitas = driver.find_element(By.XPATH,"//span[@class='post-visits']").get_attribute('innerHTML')
        driver.close()

        d.append((headline,Autor,visitas,Fecha,Link))

        #print(headline,"//",Autor,'//',Fecha,"//",Link,"//",visitas)
        
    except:
       pass


# Convertimos el scraper en un Dataframe 
DF = pd.DataFrame(d,columns=('Headline','Autor','visitas','Fecha','Link'))


# Separamos las Columnas Fecha y Hora
DF[['Fecha','Hora']] = DF['Fecha'].str.split('|', expand = True)
# Separamos las Columnas en Fecha y Año
DF[['Fecha','Año']] = DF['Fecha'].str.split(',', expand= True)


# Separamos las Columnas en Fecha y Año

subDF = DF['Fecha'].str.split(' ', expand=True)
subDF


# Juntamos el sub data frame con el data frame original:


finalDF = pd.concat([DF, subDF], axis=1)
finalDF


# Renombrando las nuevas columnas:


finalDF.columns=["Headline", "Autor", "visitas", "Fecha", "Link", "Hora", "Año", "Dia_semana", "Dia_numerico", "Mes"]


#Ordenamos las Columnas
finalDF.drop(['Fecha'], axis=1, inplace=True)


df = finalDF


# Cambiar el tipo de variables


df['visitas'] = df['visitas'].apply(lambda x: str(x.split()[0].replace(',', '.')))


df['visitas'] = df['visitas'].astype(float)


df['Año'] = df['Año'].astype(int)


df['Headline'] = df['Headline'].astype(str)


df['Autor'] = df['Autor'].astype(str)


df['Dia_semana']= df['Dia_semana'].astype(str)


df['Dia_numerico']= df['Dia_numerico'].astype(float)


df['Mes']= df['Mes'].astype(str)


# Ordenamos el dataframe por numero de visitas


Mas_vistas = df.head(10).sort_values(by='visitas',ascending=False)



# Para saber la cantidad de filas y columnas:


df.shape


# Pasando a csv


df.to_csv('Noticias_diarias.csv',encoding='utf-8-sig')
