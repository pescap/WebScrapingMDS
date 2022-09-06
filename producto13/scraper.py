from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from functools import reduce
from datetime import date
import logging
import time
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--headless')
driver = webdriver.Chrome(options= options)



def logger(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == 'main':
            logging.info(f'Processing location: {args[1]}')
        else:
            logging.info(f'\tRunning function: {func.__name__}')
        result = func(*args, **kwargs)
        return result
    
    return wrapper



@logger
def main(driver, comuna):
    frames = []
    urls = get_all_pages(driver, comuna)
    for i, u in enumerate(urls):
        logging.info(f'\tIndice: {i} ')
        name = get_name(driver, u)
        price = get_price(driver, u)
        features = get_features(driver, u)
        location = get_location(driver, u)
        metro = get_metro_station(driver, u)
        data_frames = [name, price, location, features, metro]
        frame = merge_frames(data_frames)
        frames.append(frame)

    df = pd.concat(frames, axis= 0, ignore_index= True)

    comuna = comuna.split("-")[:-1]
    df['comuna'] = ' '.join(comuna)
    df['fecha'] = date.today()
    df.to_csv(f"results/{comuna[0]}_{str(date.today())}.csv",sep = ";", 
              index= False, 
              encoding= 'latin1'
    )
    
    return 



def get_page_number(url):
    driver.get(url)
    try:
        resp = driver.find_element(By.CLASS_NAME,"andes-pagination__page-count")
        n_pages = int(resp.text.replace("de ",""))
        page_list = list(range(1, n_pages * 50 + 1, 50))
        return page_list
    except:
        return [1]



def get_all_pages(driver, place):
    PATH = "https://www.portalinmobiliario.com/arriendo/departamento"
    page_list = get_page_number(f"{PATH}/{place}")
    urls = []
    
    for page in page_list:
        driver.get(f"{PATH}/{place}/Desde_{page}")
        for i in driver.find_elements(By.CSS_SELECTOR, "a.ui-search-result__image"):
            url = i.get_attribute("href")
            
            urls.append(url)        
        
    return urls



@logger
def get_name(driver, url):
    driver.get(url)
    name = driver.find_element(By.CLASS_NAME, "ui-pdp-title").text
    
    result = pd.DataFrame([{'nombre':name, 'url':url}])
     
    return result



@logger
def get_price(driver, url):
    driver.get(url)
    price = driver.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text

    result = pd.DataFrame([{'precio':price, 'url':url}])
    
    return result



@logger
def get_published(driver, url):
    driver.get(url)
    published = driver.find_element(By.CLASS_NAME,"ui-pdp-seller-validated").find_element(By.TAG_NAME,"p").text

    result = pd.DataFrame([{'publicado':published, 'url':url}])
    
    return result



@logger
def get_location(driver, url):
    driver.get(url)
    location = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui-vip-location")))
    location = WebDriverWait(location,10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    location_text = location.get_attribute("innerHTML")
    
    result = pd.DataFrame([{'dirección':location_text, 'url':url}])
    
    return result



@logger
def get_features(driver, url):
    driver.get(url)
    table = driver.find_elements(By.CLASS_NAME,"andes-table__row")
    features = {'url':url}
    for element in table:
        header = element.find_element(By.TAG_NAME,"th")
        value = element.find_element(By.TAG_NAME,"td").find_element(By.TAG_NAME,"span")        
        features[header.get_attribute("innerHTML")] = value.get_attribute("innerHTML")
        
    df = pd.DataFrame([features])

    return df



@logger
def get_metro_station(driver, url):
    driver.get(url)
    section = driver.find_elements(By.CSS_SELECTOR, "div.ui-vip-poi__subsection")

    results = {
        "Distancia": [],
        'Estaciones de metro':[]
        
    }

    for i in section:
        title = i.find_element(By.TAG_NAME,"span").get_attribute("innerHTML")
        headers = i.find_elements(By.CSS_SELECTOR,"div.ui-vip-poi__item-title")
        subtitles = i.find_elements(By.CSS_SELECTOR,"div.ui-vip-poi__item-subtitle")
        for h in headers:
            header = h.find_element(By.TAG_NAME,"span")
            if title.strip() == 'Estaciones de metro':
                results[title].append(header.get_attribute("innerHTML"))
        for s in subtitles:
            subtitile = s.find_element(By.TAG_NAME,"span")
            if title.strip() == 'Estaciones de metro':
                results['Distancia'].append(subtitile.get_attribute("innerHTML"))


    results['url'] = [url] * len(results["Distancia"])
    df = pd.DataFrame(results)
    
    try:
        df = df.iloc[[0],:]
        return df
    except:
        return df
    


@logger
def merge_frames(data_frames):
    df_merged = reduce(lambda left,
                              right: pd.merge(left,right,
                              on=['url'],
                              how='outer'), 
                              data_frames
    )
    
    return df_merged




if __name__ == '__main__':
    start_time = time.time()
    LOCATION = 'renca-metropolitana'
    main(driver, LOCATION)
    print("--- %s seconds ---" % (time.time() - start_time))
    driver.close()


logging.info('PROCESO FINALIZADO')

