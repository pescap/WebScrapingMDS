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


def scraper(url, list_anios, list_meses, list_dias=None):
    """Scraper"""
    chrome_options = Options()
    path = os.path.join(os.getcwd(), "output")
    prefs = {"download.default_directory" : path,  "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    driver.implicitly_wait(10)

    Integraciones = driver.find_element(By.XPATH, "/html/body/section/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div[1]/div[2]/div[1]/div/div/div[3]/div/div/a[6]")
    Integraciones.click()

    url_downloads = []

    # Loop de anios
    for anio in list_anios:
        select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[1]/div/select', str(anio))

        # Loop de meses
        for mes in list_meses:
            select_option(driver, '/html/body/div[11]/div/div/div[2]/form/div[2]/div[2]/div/select', mes)
            select = Select(driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[2]/form/div[2]/div[3]/div/select")) #get all the options into a list
            options_list = [item.get_attribute("value") for item in select.options]

            # Obtencion de dias a considera para la consulta
            option_dias = compare_lists(options_list, list_dias) if list_dias is not None else options_list

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


def main():
    url = 'https://www.pjud.cl/tribunales/corte-suprema'
    list_anios = ['2022']
    list_meses = ['01']

    list_urls = scraper(url, list_anios, list_meses)

    dir_output = os.path.join(os.getcwd(), "output")
    downloader_files(list_urls, dir_output)


if __name__ == "__main__":
    main()
