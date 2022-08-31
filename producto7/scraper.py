from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import sys
import locale




os.environ['w2n.lang'] = 'es'
locale.setlocale(locale.LC_TIME, 'es_ES')

def fill_text_field(driver, xpath, text):
    # Funcion que llena texto en un campo de la pagina
    text_input = driver.find_element(By.XPATH, xpath)
    text_input.clear()
    text_input.send_keys(text)

def select_option(driver, xpath, index):
    # Selecciona una opcion en un menu desplegable
    select_object = Select(driver.find_element(By.XPATH, xpath))
    select_object.select_by_value(index)


url = 'https://www.pjud.cl/tribunales/corte-suprema'
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output\\")
prefs = {"download.default_directory" : path,  "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = chromeOptions)
driver.get(url)

driver.implicitly_wait(10)

anos = ["2015", "2016", "2017", "2018", "2019"]
meses = ["01", "02", "03", "04", "05", "06", "07", "08", '09', '10', '11', '12']



for ano in anos:
    # Estos indices se obtienen de las opciones de la pagina, cada uno es un mes, cambiar para obtener mas meses
    #for index in range(1, 2):
        # Se envia la info a la pagina
    select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[1]/div/select', str(ano))
    for mes in meses:
        select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[2]/div/select', mes)
        select = Select(driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[2]/form/div[2]/div[3]/div/select")) #get all the options into a list
        optionsList = []
        for item in select.options:
            optionsList.append(item.get_attribute("value"))            
            for optionValue in optionsList:
                select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[3]/div/select', optionValue)

        # Se hace click con los datos llenados
                driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[4]/button').click()
        
        # Se descargan los datos
                wait = WebDriverWait(driver, 10) 
    #descarga por salas cambia último tr: 1, 2, 3, 4 - no siempre está disponible, el mismo día, las mismas salas
                try: 
                    boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[11]/div/div/div[2]/table/tbody/tr[1]/td[1]/a')))
                    boton_descarga.click()
                except: 
                    pass
                try: 
                    boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[11]/div/div/div[2]/table/tbody/tr[2]/td[1]/a')))
                    boton_descarga.click()
                except: 
                    pass
                try: 
                    boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[11]/div/div/div[2]/table/tbody/tr[3]/td[1]/a')))
                    boton_descarga.click()
                except: 
                    pass
                try: 
                    boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[11]/div/div/div[2]/table/tbody/tr[4]/td[1]/a')))
                    boton_descarga.click()
                except: 
                    pass
driver.close