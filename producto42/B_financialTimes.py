from bs4 import BeautifulSoup
import json
import lxml
import re
import requests
import pandas as pd
import sys
from tqdm import tqdm

# Inputs
flag_ = False
while not flag_:
    instrumento = input("Ingrese instrumento: ")
    
    # Para obtener num total de paginas de resultados de la busqueda
    url_name = f"https://www.ft.com/search?q={instrumento}&page=1&contentType=article&sort=relevance&expandRefinements=true"
    
    url = requests.get(url_name)
    soup = BeautifulSoup(url.text, "html.parser")
    
    paginacion = soup.find("span", class_= "search-pagination__page")
    numPaginasTotales = int(paginacion.text.split()[3])
    print(f"Hay un total de {numPaginasTotales} paginas --> {numPaginasTotales*25} articulos aprox")
    
    numPaginas = int(input("Cuantas paginas de resultados desea scrapear?: ")) 
    print(f"Serian aprox. {25*numPaginas} articulos en {divmod(16*numPaginas,60)[0]}:{divmod(16*numPaginas,60)[1]} minutos aprox.")
    
    continuar = input("Desea Continuar? [y]/n: ")
    print()
    
    if continuar == "y": 
        flag_ = True
    else: 
        pass


numPaginas += 1

# Prealocacion de listas
links = []
titulos = []
fechas = []
cuerpo = []

# Preliminares del ciclo for
rango = [i for i in range(1, numPaginas)]


# EJECUCION
for pagina in tqdm(rango, desc='Paginas de Resultados Scrapeadas'): # ciclo for cada cada pagina de resultados de la busqueda por instrumento
    url_name = f"https://www.ft.com/search?q={instrumento}&page={pagina}&contentType=article&sort=relevance&expandRefinements=true"

    # Se define objeto BeautifulSup
    url = requests.get(url_name)
    soup = BeautifulSoup(url.text, "html.parser")
    
    for article in (soup.find_all("div", class_="o-teaser__content")):
        
        # Se obtiene Link de articulo
        content = article.find("a", class_ = "js-teaser-heading-link", href=True)
        link = "https://www.ft.com" + content["href"]
        links.append(link)
        
        # Se entra en el link
        url = requests.get(link)
        soup = BeautifulSoup(url.text, "html.parser")
        
        # Se obtiene json (que es la forma que tiene ft para el paywall). Este json contiene todo lo relacionado con la noticia
        data = [json.loads(i.string) for i in soup.find_all("script", type="application/ld+json")]
                
        # Se obtienen las partes especficias del json
        for i in data:
            try:
                body = i["articleBody"] 
                fecha = i["datePublished"]
                titulo = i["headline"]
            except KeyError: 
                pass
        
        cuerpo.append(body)
        titulos.append(titulo)
        fechas.append(fecha)
        
        
# Se crea diccionario con todos los datos obtenidos
diccDF = {"Titulo": titulos, "Fecha": fechas, "Link": links, "Body": cuerpo}

# Se tranforma diccionario a Data Frame
df = pd.DataFrame(diccDF)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# df.to_csv(f'C:/Users/psini/Desktop/Web_Scrapping/ft/prueba/{instrumento}_{numPaginas-1}.csv', encoding='utf-8', index=False, header=True)
# print("Listo!")
# print(f"Se obtuvieron {len(df)} articulos")



