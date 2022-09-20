from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import lxml


# Ingreso de URL
url = "https://finviz.com/quote.ashx?t="

instrumento = input("Ingresar instrumento en minuscula: ")
instrumentoUpper = instrumento.upper()


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
horas = []
dias = []
titulares = []

for articulo in  tabla.find_all("tr"): # para cada fila del tablon de noticias
    
    # Fecha
    #=================================================
    fecha = articulo.find("td").string.split() 
    
    # Dia 
    if len(fecha) == 2:
        dia = fecha[0]
   
    dias.append(dia)
    
    # Hora      
    if len(fecha) == 1:
        horas.append(fecha[0])
    elif len(fecha) == 2:
        horas.append(fecha[1])
        
    # Titular
    titular = articulo.find("a").string   
    titulares.append(titular)

# Operaciones para ordenar DF 
diccDF = {"Dia": dias, "Horas": horas, "Titular": titulares}
df = pd.DataFrame(diccDF)

df["Fecha"] = pd.to_datetime(df["Dia"] + " " + df["Horas"])
df.drop(["Dia", "Horas"], axis=1, inplace=True)

df = df[["Fecha", "Titular"]]
# ========================================= 
# se genera csv
print("Generando CSV...")
df.to_csv(f"output/{instrumento}_finviz.csv", encoding='utf-8', index=False)
print("Listo!")

