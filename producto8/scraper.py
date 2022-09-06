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

#Configuraciones estandar para poder ejecutar el navegador web
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output\\")
prefs = {"download.default_directory" : path, "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs",prefs)

### URL del sitio web desde el que se extraerá la información
URL = 'https://www.portalinmobiliario.com/arriendo/departamento/vina-del-mar-valparaiso'

#Abrir el navegador e ingresar a la URL de Interes
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)

driver.find_element(By.XPATH,"/html/body/div[2]/div/button").click()

### Ingreso de parámetros (filtros)

## Selección de los barrios de interés

# Barrio 1
driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section/div[5]/ul/li[2]/a/span[1]').click()

# Barrio 2
driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[4]/ul/li[8]/a/span[1]').click()

# Barrio 3
driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[4]/ul/li[7]/a/span[1]').click()


## Variables de String a utilizar

precio_max = 700000 # máximo 700.000 CLP
piezas = 2  # mínimo 2 habitaciones


# Ingresar precio máximo de arriendo
input_precio_max = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[5]/ul/li[5]/form/div[2]/div/label/div[2]/input')
input_precio_max.send_keys(precio_max)
input_precio_max.send_keys(Keys.ENTER)

# Ingresar cantidad mínima de habitaciones
input_piezas = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/section[2]/div[7]/ul/li[5]/form/div[1]/div/label/div[2]/input')
input_piezas.send_keys(piezas)
input_piezas.send_keys(Keys.ENTER)

# Botón criterio de orden: //*[@id="root-app"]/div/div[2]/section/div[1]/div/div/div[2]/div[2]/div/button/span

# Abrir menú de criterio de orden
ordenar_resultados = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/section/div[1]/div/div/div[2]/div[2]/div/button')
ordenar_resultados.click()

driver.find_element(By.XPATH ,'//*[@id="andes-dropdown-más-relevantes-list-option-price_asc"]/div/div/span').click()



#ordenar = Select(ordenar_resultados)

# Seleccionar ordenar por menor precio
#ordenar.select_by_visible_text('Menor precio')
