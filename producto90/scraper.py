"""
Autor: Manuel Oliva
"""
#!pip install webdriver
#!pip install ChromeDriverManager
#!pip install webdriver_manager

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os


chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')

# Se define la ruta
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output/")
# Se borra informacion irrelevante.
for file in os.listdir(path):
    if 'vcfA2022-2022.csv' in file: 
        os.remove(os.path.join(path, file)) 
    if 'vcfB2022-2022.csv' in file: 
        os.remove(os.path.join(path, file))
    if 'vcfC2022-2022.csv' in file: 
        os.remove(os.path.join(path, file))
    if 'vcfD2022-2022.csv' in file: 
        os.remove(os.path.join(path, file))
    if 'vcfE2022-2022.csv' in file: 
        os.remove(os.path.join(path, file))

fondos=['A','B','C','D','E']
type(fondos)
for a in fondos:

    # URL de la cual podemos obtener la informacion
    URL = 'https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php?tf='+ str(a)
    
    
    # Se define la ruta de descarga
    chromeOptions = webdriver.ChromeOptions()
    path = os.path.join(os.getcwd(), "output/")
    prefs = {"download.default_directory" : path,  "directory_upgrade": True}
    chromeOptions.add_experimental_option("prefs",prefs)
    
    
    
    # Se instala chromeDriverManager, se puede ajustar una vez se corre por primera vez
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = chromeOptions)
    driver.get(URL)
    
    # Se descargan los datos
    wait = WebDriverWait(driver, 10)
    boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, 'html/body/div[5]/div/div[2]/div/div[2]/table[2]/tbody/tr[11]/td/table/tbody/tr/td[3]/a/img')))
    boton_descarga.click()
    
    # Tiempo de descarga
    time.sleep(1)
    driver.back()
driver.close()

