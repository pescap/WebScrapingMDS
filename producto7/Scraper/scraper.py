from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request
import requests
import pandas as pd
import io

os.environ['w2n.lang'] = 'es'

def fill_text_field(driver, xpath, text):
    """Funcion que llena texto en un campo de la pagina"""
    text_input = driver.find_element(By.XPATH, xpath)
    text_input.clear()
    text_input.send_keys(text)


def select_option(driver, xpath, index):
    """Selecciona una opcion en un menu desplegable"""
    select_object = Select(driver.find_element(By.XPATH, xpath))
    select_object.select_by_value(index)


def compare_lists(list1, list2):
    """Funcion que compara dos listas y retorna una lista de la diferencia entre ellas"""
    return list(set(list1) - set(list2))


def scraper(url, list_anios, dict_mes_dias):
    """Scraper"""
    chrome_options = Options()
    path = os.path.join(os.getcwd(), "output")
    prefs = {"download.default_directory" : path,  "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
    driver.get(url)

    driver.implicitly_wait(10)

    Integraciones = driver.find_element(By.XPATH, "/html/body/section/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div[1]/div[2]/div[1]/div/div/div[3]/div/div/a[6]")
    Integraciones.click()

    url_downloads = []

    # Loop de anios
    for anio in list_anios:
        select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[1]/div/select', str(anio))
        select_mes = Select(driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[2]/div/select')) #get all the options into a list
        options_meses_list = [item.get_attribute("value") for item in select_mes.options]
        options_meses_list.remove('null')
        list_meses = list(dict_mes_dias.keys()) # meses ya scrapeados
        # Obtencion de meses a considerar para la consulta
        option_meses = compare_lists(options_meses_list, list_meses)

        # Loop de meses
        for mes in option_meses:
            select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[2]/div/select', mes)
            select_dias = Select(driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[2]/form/div[2]/div[3]/div/select")) #get all the options into a list
            options_dias_list = [item.get_attribute("value") for item in select_dias.options]
            options_dias_list.remove('null') 
            list_dias = dict_mes_dias[mes] if mes in dict_mes_dias.keys() else []  # dias ya scrapeados

            # Obtencion de dias a considera para la consulta
            option_dias = compare_lists(options_dias_list, list_dias)

            # Loop de dias a consultar
            for optionValue in option_dias:
                select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[3]/div/select', optionValue)
                driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[4]/button').click()
                wait = WebDriverWait(driver, 10) 

                # Loop que recorre las 4 salas 
                for i in range(1,5):
                    try:
                        boton_descarga = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/div[11]/div/div/div[2]/table/tbody/tr[{i}]/td[1]/a")))
                        url_downloads.append(boton_descarga.get_attribute('href'))  # Agrega link de descarga a lista
                    except: 
                        pass
    driver.close

    return url_downloads


def downloader_files(list_urls, dir_output):
    """Recibe la lista de urls para descarga de los archivos de pdf y los guarda en la carpeta dada"""

    for url_file in list_urls:
        urllib.request.urlretrieve(url_file, f"{dir_output}/acta_{''.join(filter(str.isdigit, url_file))}.pdf")


def get_periodo(dir):
    """Obtiene la lista de meses y dias ya escrapeados"""
    df = pd.read_csv(dir)
    df['dia'] = pd.to_datetime(df['Fecha2']).dt.day.map("{:02}".format)
    df['mes'] = pd.to_datetime(df['Fecha2']).dt.month.map("{:02}".format)

    list_meses = df['mes'].unique().tolist()
    dict_mes_dias = {}
    for mes in list_meses:
        dict_mes_dias[mes] = df[df['mes'] == mes]['dia'].unique().tolist()

    return dict_mes_dias

def main():
    
    url = 'https://www.pjud.cl/tribunales/corte-suprema'
    list_anios = ['2022']
    
    dir_output = os.path.join(os.getcwd(), "output")
    dir_file = os.path.join(dir_output, "2022_01_08.csv.csv")
    dict_mes_dias = get_periodo(dir_file)

    list_urls = scraper(url, list_anios, dict_mes_dias)
    downloader_files(list_urls, dir_output)


if __name__ == "__main__":
    main()
