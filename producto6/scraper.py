#!/usr/bin/env python
# coding: utf-8

# # Librerias

# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen

from lxml import etree
import xml.etree.ElementTree as ETree

import pandas as pd
import time

import datetime

import os

from selenium import webdriver

from webdriver_manager.chrome          import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver         import ActionChains


# # Carpeta para el Producto

# In[2]:


# Creamos carpeta para el Producto Analizado
#CurrentDirectory = os.getcwd()
#CurrentDirectoryFolder = CurrentDirectory + '\\' + 'FALABELLA' #PARAMETRO_NOMBRE


# In[3]:


# Ve si existe la carpeta del Producto Analizado, o la crea

#if os.path.exists(CurrentDirectoryFolder) == True:
#    print('Existe')
#else:
#    os.makedirs(CurrentDirectoryFolder)
#    print('Creada, ahora existe')


# # Parametros para Selenium

# In[4]:


# definir ruta_descarga a gusto
#ruta_descarga = CurrentDirectoryFolder 
path = os.path.join(os.getcwd(), "output")


options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": path, #Donde descargara
  "download.prompt_for_download": False,
  "download.directory_upgrade": True
})
options.add_argument('--headless')
#https://stackoverflow.com/questions/46937319/how-to-use-chrome-webdriver-in-selenium-to-download-files-in-python


# In[5]:


# Initiate the browser
browser  = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


# # Navegacion y Descarga

# In[6]:


# Open the Website
browser.get('https://www.investing.com/equities/falabella')


# Open the Website
# browser.get('https://www.investing.com/')

# Matar el popup
# try:
#     WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.popupCloseIcon.largeBannerCloser"))).click()
# except TimeoutException as to:
#     print(to)

# Buscaremos la empresa que nos interesa
# browser.find_element(By.XPATH, '/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input').send_keys('FALABELLA')
# browser.find_element(By.XPATH, '/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input').send_keys(Keys.ENTER)
# time.sleep(5)

# In[ ]:





# # Navegacion

# In[7]:


# Baja una Pantalla
browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(5)


# In[8]:


# Ingresa a Data Historica
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[7]/nav/ul/li[3]/a').click()
#browser.find_element(By.XPATH, '/html/body/div/div[1]/header/div[3]/div/div/div/div/form/div[1]/button').click()


# In[9]:


# Baja una Pantalla
browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(5)


# In[10]:


# Matar el otro popup
browser.find_element(By.XPATH, '/html/body/div/div[1]/header/div[3]/div/div/div/div/form/div[1]/button').click()


# In[11]:


# Click en el buscador de fechas
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div/div[2]').click()


# In[12]:


# Pasos para forzar 01-01-2022
# Si se quiere buscar Febrero 2022 -> 01/02/2022
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').click()
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').clear()
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').send_keys('01/01/2022')
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').clear()
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').send_keys('01/01/2022')
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/input').click()
browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/button').click()


# # Scrapear Tabla
# 
# Con el Navegador ya abierto e interactuado

# In[13]:


time.sleep(15)
#browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
#browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
#browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
#browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
#browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[3]/div/table/tbody').click()


# In[14]:


source = browser.page_source


# In[15]:


content_page = BeautifulSoup(source, "html.parser")


# In[16]:


# dom = etree.HTML(str(content_page))


# In[17]:


# la ruta es: //*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[3]/div/table/tbody
# El //text() es para que me regrese todos los textos
# datos = dom.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[8]/div/div/div[3]/div/table/tbody//text()')


# In[18]:


# Extraemos la tabla y la guardamos en una lista
contador = 0

valores = content_page.find_all('tbody', {'class':'datatable_body__3EPFZ'})

for valor in valores[1]: #Es la segunda la que nos interesa
    for val in valor:
        
        contador = contador + 1
    
        if contador == 1:
            Raw_Data = pd.DataFrame({'valor':val.get_text()}, index=[contador-1])
        else:
            Raw_Data = pd.concat([Raw_Data, pd.DataFrame({'valor':val.get_text()}, index=[contador-1]) ])
        
        #print(val.get_text())


# In[19]:


# Separamos la lista anterior en un dataframe trabajable
i = 0
j = 0

iteraciones = int(len(Raw_Data)/7)


cols = ['Date', 'Price', 'Open', 'High', 'Low', 'Vol', 'ChangePercent']
datos_df = pd.DataFrame(columns=cols, index=range(iteraciones))

while iteraciones > j:

    datos_df.loc[j].Date          = Raw_Data.valor.loc[i + 0]
    datos_df.loc[j].Price         = Raw_Data.valor.loc[i + 1]
    datos_df.loc[j].Open          = Raw_Data.valor.loc[i + 2]
    datos_df.loc[j].High          = Raw_Data.valor.loc[i + 3]
    datos_df.loc[j].Low           = Raw_Data.valor.loc[i + 4]
    datos_df.loc[j].Vol           = Raw_Data.valor.loc[i + 5]
    datos_df.loc[j].ChangePercent = Raw_Data.valor.loc[i + 6]
                      
    i = i + 7
    j = j + 1


# In[20]:


# Limpiaremos la Informacion
datos_df_limpio = datos_df.copy()


# In[21]:


datos_df_limpio['Date']          = pd.to_datetime(datos_df_limpio['Date'].astype(str) , format= '%m/%d/%Y')
datos_df_limpio['Price']         = datos_df_limpio['Price'].str.replace(',','').astype('float')
datos_df_limpio['Open']          = datos_df_limpio['Open'].str.replace(',','').astype('float')
datos_df_limpio['High']          = datos_df_limpio['High'].str.replace(',','').astype('float')
datos_df_limpio['Low']           = datos_df_limpio['Low'].str.replace(',','').astype('float')
datos_df_limpio['ChangePercent'] = datos_df_limpio['ChangePercent'].str.replace('%','').astype('float')


import openpyxl
# Exportamos Resultado -- Cambiar Ruta a ruta del proyecto


#datos_df_limpio.to_excel(CurrentDirectoryFolder + '\\' + 'FALABELLA.xlsx', index=False) #PARAMETRO_NOMBRE

datos_df_limpio.to_csv('output/output.csv', index = False)
browser.close()


# #### Pendiente... quizas
# Que lea el archivo anterior (En caso de existir) y le pege solo los valores nuevos

# In[ ]:




