#!/usr/bin/env python
# coding: utf-8

# In[60]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select # no hara operaciones hasta q se carguen los elementos de la página
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os 
from datetime import date


# In[56]:


def guarda_csv(df, titulo):
    fecha_data = date.today()
    nombre_archivo = fecha_data.strftime('%Y%m%d') + titulo + '.csv' 
    file_dir = os.path.dirname(os.path.abspath("_file_"))
    csv_folder = 'output/' + fecha_data.strftime('%Y') + "/" + fecha_data.strftime('%m')
    try:
        os.makedirs(os.path.join(file_dir, csv_folder))
    except FileExistsError:
        pass
    file_path = os.path.join(file_dir, csv_folder, nombre_archivo)
    df.to_csv(file_path, index=False)
    print('Archivo guardado', nombre_archivo)
    print("")


# In[40]:


# Opciones de navegacion

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

# Inicialimos el navegador 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.lider.cl/supermercado/")



# In[41]:


# Digitaremos la palabra azúcar y daremos click en buscar de forma automatica:
WebDriverWait(driver,5)    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#searchtextinput")))    .send_keys("azucar")

WebDriverWait(driver,5)    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button#searchsubmitbutton")))    .click()


# In[42]:


print(driver.current_url)


# In[43]:


#Funcion para capturar los objetos por etiqueta y clase
def buscar_tag_por_etiqueta_clase(html, etiqueta, clase):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all(etiqueta, class_= re.compile(clase +"$"))
 


# In[44]:


class Producto:
    pass


# In[45]:


#usaremos request para consultar por una dirección url y obtener el contenido, en este caso leer productos de supermecado lider
# y en vez de llamar a la página WEb a través del dominio llamamos a través de driver.current 
ruta = driver.current_url
sitio = requests.get(ruta)


# In[46]:


#Buscamos nuestros tag que contienen los productos del carro
listado_items = buscar_tag_por_etiqueta_clase(sitio.content, "div", "product-item-box")


# In[47]:


#Ahora vamos a recorrer cada producto del carro, según la lista que encontramos en el paso anterior. Generamos una lista de productos donde 
#guardaremos nuestros objeto Producto, según los valores que rescatamos dentro del ciclo for

productos = []
for i in listado_items:
    producto = Producto()

        
    if (i.find('span', class_="product-description js-ellipsis", recursive=True) != []):
        producto.nombre = i.find('span', class_="product-description js-ellipsis", recursive=True).text
    
    if (i.find('span', class_="product-name", recursive=True) != []):
        producto.marca = i.find('span', class_="product-name", recursive=True).text
      
    
        
    if (i.find('span', class_="price-sell", recursive=True) != []):
        producto.precio = i.find('span', class_="price-sell", recursive=True).text

    producto.origen = "Lider"
    producto.fecha_captura = datetime.date.today().strftime("%Y-%m-%d")
    
    if (i.find('span', class_="product-attribute", recursive=True) != []):
        producto.formato = i.find('span', class_="product-attribute", recursive=True).text
        
    productos.append(producto)


# In[48]:


#Creamos un dataframe a partir de nuestra lista de productos capturados en el paso anterior
df = pd.DataFrame.from_records([t.__dict__ for t in productos ])
df.head(200)


# In[50]:


df2 =df[df.marca.isin(["Lider","Iansa"])]
df3 =df2[df2["nombre"]!="Merluza Filetes Con Piel"]


# In[51]:


# Ahora ordenamos el DataFrame por marca:
df3.sort_values("marca")


# In[59]:


guarda_csv(df3,"lider")


# In[13]:


# Web Scrapping página Tottus:

# Opciones de navegacion

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

# Inicialimos el navegador 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://tottus.falabella.com/tottus-cl")


# In[14]:


# Digitaremos la palabra azúcar y daremos click en buscar de forma automatica:
WebDriverWait(driver,5)    .until(EC.element_to_be_clickable((By.CLASS_NAME,"SearchBar-module_searchBar__Input__1kPKS")))    .send_keys("azucar")

WebDriverWait(driver,5)    .until(EC.element_to_be_clickable((By.CLASS_NAME,"SearchBar-module_searchBtnIcon__2L2s0")))    .click()


# In[15]:


print(driver.current_url)


# In[16]:


# Web Scrapping página Tottus:

#Funcion para capturar los objetos por etiqueta y clase
def buscar_tag_por_etiqueta_clase(html, etiqueta, clase):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all(etiqueta, class_= re.compile(clase +"$"))
 


# In[ ]:





# In[17]:


class Producto:
    pass


# In[20]:


#usaremos request para consultar por una dirección url y obtener el contenido, en este caso leer productos de supermecado Jumbo
ruta = driver.current_url
sitio = requests.get(ruta)


# In[21]:


#Buscamos nuestros tag que contienen los productos del carro
listado_items_tottus = buscar_tag_por_etiqueta_clase(sitio.content, "div", "grid-pod")
print(len(listado_items_tottus))


# In[22]:


#Ahora vamos a recorrer cada producto del carro, según la lista que encontramos en el paso anterior. Generamos una lista de productos donde 
#guardaremos nuestros objeto Producto, según los valores que rescatamos dentro del ciclo for

productos = []
for i in listado_items_tottus:
    producto = Producto()

        
    if (i.find('b', class_="subTitle-rebrand", recursive=True) != []):
        producto.nombre = i.find('b', class_="subTitle-rebrand", recursive=True).text
        
    if (i.find('span', class_="line-height-22", recursive=True) != []):
        producto.precio = i.find('span', class_="line-height-22", recursive=True).text
        
    if (i.find('b', class_="title-rebrand", recursive=True) != []):
        producto.marca = i.find('b', class_="title-rebrand", recursive=True).text
    
    
    producto.origen = "Tottus"
    producto.fecha_captura = datetime.date.today().strftime("%Y-%m-%d")
    productos.append(producto)


# In[37]:


#Creamos un dataframe a partir de nuestra lista de productos capturados en el paso anterior
df = pd.DataFrame.from_records([t.__dict__ for t in productos ])
df.head(200)


# In[38]:


df[["nombre","formato"]]= df["nombre"].str.split("-",expand=True)
df


# In[52]:


def guarda_csv(df, titulo):
    fecha_data = date.today()
    nombre_archivo = fecha_data.strftime('%Y%m%d') + titulo + '.csv' 
    file_dir = os.path.dirname(os.path.abspath("_file_"))
    csv_folder = 'output/' + fecha_data.strftime('%Y') + "/" + fecha_data.strftime('%m')
    try:
        os.makedirs(os.path.join(file_dir, csv_folder))
    except FileExistsError:
        pass
    file_path = os.path.join(file_dir, csv_folder, nombre_archivo)
    df.to_csv(file_path, index=False)
    print('Archivo guardado', nombre_archivo)
    print("")


# In[61]:


guarda_csv(df,"tottus")

