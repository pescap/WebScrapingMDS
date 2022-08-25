from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os


def fill_text_field(driver, xpath, text):
    # Funcion que llena texto en un campo de la pagina
    text_input = driver.find_element(By.XPATH, xpath)
    text_input.clear()
    text_input.send_keys(text)

def select_option(driver, xpath, index):
    # Selecciona una opcion en un menu desplegable
    select_object = Select(driver.find_element(By.XPATH, xpath))
    select_object.select_by_value(index)

# URL de la cual podemos obtener la informacion
URL = 'https://climatologia.meteochile.gob.cl/application/requerimiento/producto/RE1006'


# Se define la ruta de descarga
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output\\")
prefs = {"download.default_directory" : path,  "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs",prefs)


#driver = webdriver.Chrome(executable_path=DRIVER_PATH, options = chromeOptions)
#driver.get(URL)

# Se instala chromeDriverManager, se puede ajustar una vez se corre por primera vez
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = chromeOptions)
driver.get(URL)

# Estacion 330020 es quinta normal
estacion = '330020'

# Años a usar (primera linea es un scrapeo exhaustivo, para ver el funcionamiento se recomienda solo correr la segunda linea)
años = list(range(1990, 2022))
#años = [2021]
for año in años:
    # Estos indices se obtienen de las opciones de la pagina, cada uno es un mes, cambiar para obtener mas meses
    for index in range(1, 2):
        # Se envia la info a la pagina
        fill_text_field(driver, '/html/body/div/form/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/input', estacion)
        fill_text_field(driver, '/html/body/div/form/div/div[1]/div/div[2]/div[1]/div[3]/div/input', año)
        select_option(driver, '/html/body/div/form/div/div[1]/div/div[2]/div[1]/div[5]/div/select', str(index))

        # Se hace click con los datos llenados
        driver.find_element(By.XPATH, ' /html/body/div/form/div/div[1]/div/div[2]/div[1]/div[7]/div/input').click()
        
        # Se descargan los datos
        wait = WebDriverWait(driver, 10)
        boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[3]/button[2]')))
        boton_descarga.click()

        # Tiempo de descarga
        time.sleep(1)
        
        # Se preprocesan los datos y se borra informacion irrelevante.
        for file in os.listdir(path):
            if 'Precipitación' in file: 
                df = pd.read_html(os.path.join(path, file))  
                df[0].to_csv('output/PrecipitacionesDiarias_{}_{}_{}.csv'.format(estacion, str(index), str(año)), index = False)
                os.remove(os.path.join(path, file)) 
        
        # El navegador se devuelve para obtener mas informacion
        driver.back()
driver.close()