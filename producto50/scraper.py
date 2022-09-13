# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import xlrd

def fill_text_field(driver, xpath, text):
    # Funcion que llena texto en un campo de la pagina
    text_input = driver.find_element(By.XPATH, xpath)
    text_input.clear()
    text_input.send_keys(text)

def select_option(driver, xpath, index):
    # Selecciona una opcion en un menu desplegable
    select_object = Select(driver.find_element(By.XPATH, xpath))
    select_object.select_by_value(index)


URL = "https://www.cmfchile.cl/institucional/estadisticas/fm.bpr_menu.php"

# Se define la ruta de descarga
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), "output\\")
prefs = {"download.default_directory" : path,  "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs",prefs)


# Se instala chromeDriverManager, se puede ajustar una vez se corre por primera vez
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = chromeOptions)
driver.get(URL)

#Loop fechas
años = ['2021', '2022']
meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for año in años:
    for mes in meses:
        #Loop dias
        for dia in range(1, 32):
            # Entro en form, selecciono periodicidad diaria
            select_option(driver, '/html/body/div[2]/div[2]/div/div/div/div[4]/form/div/select', '1') 
            
            # Entro en form, selecciono tipo de consulta por una fecha
            select_option(driver, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/form/div/select', '1') 
            
            #Selecciono dia
            select_option(driver, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div[1]/form/div[4]/label/select[1]', str(dia)) 
    
            #Selecciono mes
            select_option(driver, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div[1]/form/div[4]/label/select[2]', mes) 
    
            #Selecciono año
            select_option(driver, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div[1]/form/div[4]/label/select[3]', año) 
    
            #Tiempo de espera 5 segundos
            time.sleep(5)
    
            # Se hace click con los datos llenados
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div[1]/form/div[5]/input[3]').click()
    
            # Tiempo de descarga
            time.sleep(2)
    
            #Probar si descarga es valida o no hay datos
            valida = None

            try:
                valida = driver.find_element(By.XPATH, "//*[contains(text(), 'No se encuentran datos para su consulta.')]")
            except:
                print("Next")

            if valida != None:
                driver.back()

            if valida == None:
                #Lee archivo
                file = os.listdir(path)
            
            for file in os.listdir(path):
                if '_' in file:
                    xls = xlrd.open_workbook_xls(os.path.join(path, file), encoding_override='latin1')
                    sh = xls.sheet_by_index(0)
    
                    #Initialize list to hold data
                    Data = [None] * (sh.ncols)
    
                    #read column by column and store in list
                    for colnum in range(sh.ncols):
                        Data[colnum] = sh.col_values(colnum, start_rowx=10, end_rowx=None)

                    dict = {'FFMM': Data[0],
                            'RUN': Data[1],
                            'Tipo': Data[2],
                            'Administradora': Data[3],
                            'Serie': Data[4],
                            'Moneda': Data[5],
                            'Patrimonio': Data[6],
                            'Participes': Data[7],
                            'Valor_Cuota': Data[8]}
        
                    #Create dataframe
                    if dia==1:
                        df = pd.DataFrame(dict)
                        df['dia']=str(dia) + '-' + mes + '-' + año
                    else:
                        temp = pd.DataFrame(dict)
                        temp['dia']=str(dia) + '-' + mes + '-' + año
                        df = pd.concat([df, temp])
    

                    df.drop(df.tail(12).index, inplace = True)
                    os.remove(os.path.join(path, file))
                    driver.refresh()


        #Guarda CSV
        if isinstance(df, pd.DataFrame):
            df.to_csv('output/FFMM-{}-{}.csv'.format(str(mes), str(año)), index = False)
            df = None
 
#Cierra driver
driver.close()

