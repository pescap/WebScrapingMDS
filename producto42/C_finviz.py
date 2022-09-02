from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import lxml


# Ingreso de URL
url = "https://finviz.com/quote.ashx?t="

instrumento = input("Ingresar instrumento en minuscula: ")
instrumentoUpper = instrumento.upper()

numCSV = input("Ingresar numero de CSV de ese instrumento: ")

# ========================================= 
# Se genera url segun instrumento
url_name = url + instrumentoUpper

# Creacion objeto bs4# 
# Se define objeto BeautifulSup
url = requests.get(url_name, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(url.content, "lxml")
soup.prettify

# Se encuentra tablon de noticias
tabla = soup.find(id="news-table")

# ========================================= 
###### Generacion de DF ######
fechas = []
titulares = []

for articulo in  tabla.find_all("tr"): # para cada fila del tablon de noticias
    fecha = articulo.find("td").string.split() 
    titular = articulo.find("a").string
    
    fechas.append(fecha)
    titulares.append(titular)
    
diccDF = {"Fechas": fechas, "Titular": titulares}

paraCSV = pd.DataFrame(diccDF)

# ========================================= 
# se genera csv
print("Generando CSV...")

nombre = instrumento + "_" + numCSV + ".csv"

paraCSV.to_csv(f'C:/Users/psini/Desktop/Web_Scrapping/finviz/data/{nombre}', encoding='utf-8', index=False)
print("Listo!")

