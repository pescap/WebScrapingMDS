#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# Copiamos la url del periodico BIO BIO
URL=requests.get("https://www.biobiochile.cl/lista/busca-2020/categorias/nacional")
soup=BeautifulSoup(URL.text,'html.parser')


# In[3]:


# Creamos una variable que contengo los resultados de busqueda con beautiful soup
Titulares_Nacionales = soup.find("div", {"class": "results-container"})
Titulares_Nacionales


# In[4]:


# Buscamos lo que hay en cada artículo de noticia
Articulos = Titulares_Nacionales.find_all('article',{'class':'article article-horizontal article-with-square justify-content-between'})
Articulos


# In[5]:


# Creamos el driver para utilizar selenium y poder extraer el número de visitas
s = Service('C:\\Users\\colon\\Documents\\Magister Data Science\\Web Scrapping\\Proyecto Bio Bio\\chromedriver.exe')
driver = webdriver.Chrome(service=s)


# In[6]:


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


# In[7]:


# Convertimos el scraper en un Dataframe 
DF = pd.DataFrame(d,columns=('Headline','Autor','visitas','Fecha','Link'))


# In[8]:


DF


# In[9]:


# Creamos una copia para no repetir el scrapper
Df_copy = DF.copy()


# In[11]:


# Hacemos un Split a la columna Fecha
Df_copy[['Fecha','Hora']] = Df_copy['Fecha'].str.split('|', expand = True)
Df_copy[['Fecha','Año']] = Df_copy['Fecha'].str.split(',',expand=True)
Df_copy[['Fecha','Día']] = Df_copy['Fecha'].str.split(' ',1,expand=True)
Df_copy[['Día','Mes']] = Df_copy['Día'].str.split(' ',1,expand=True)


# In[12]:


# Creamoss la columna Date
Df_copy['Date'] = Df_copy["Fecha"] +' '+ Df_copy["Día"] +' ' +Df_copy['Mes']+ ',' +Df_copy['Año']


# In[ ]:


#Convertimos las visitas en numeros enteros
Df_copy['visitas'] = Df_copy['visitas'].str.replace('.', '').astype('int64')


# In[15]:


# Seleccionamos las columnas finales
Df_copy = Df_copy[['Headline','Autor','visitas','Date','Link']]


# In[26]:


# Cambiamos el nombre a la columna Fecha
Df_copy.columns = ['Headline', 'Autor', 'Visitas', 'Fecha','Link']


# In[28]:


#Visualizamos el Dataframe
Df_copy.head(3)


# In[19]:


# Autores que generan más visitas 
round(Df_copy.groupby('Autor').agg('visitas').sum().sort_values(ascending=False))


# In[20]:


# Numero de articulos publicado por autores
Df_copy['Autor'].value_counts()


# In[23]:


# 10 noticias más visitadas del día
Mas_vistas = Df_copy.head(10).sort_values(by='visitas',ascending=False)
print(Mas_vistas[['Headline','visitas']])


# In[24]:


Df_copy.to_csv('AAAMartes_20.csv',encoding='utf-8-sig')

