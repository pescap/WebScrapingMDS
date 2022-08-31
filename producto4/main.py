from bs4 import BeautifulSoup
import pandas as pd
import re
import requests


url_name = 'https://www.portalinmobiliario.com/venta/departamento/propiedades-usadas/providencia-metropolitana#applied_filter_id%3DOPERATION_SUBTYPE%26applied_filter_name%3DModalidad%26applied_filter_order%3D5%26applied_value_id%3D244562%26applied_value_name%3DPropiedades+usadas%26applied_value_order%3D1%26applied_value_results%3D4132%26is_custom%3Dfalse'

url = requests.get(url_name)

soup = BeautifulSoup(url.text,"html.parser")

print("esto se ejecuto")

#<span class="price-tag-fraction">5.200</span>

precio = soup.find("span", attrs={"class": "price-tag-fraction"}).get_text()

print(precio)




## Objetivo 1: Extraer UF, M2, N° dormitorios de publicaciones primera pagina

## Objetivo 2: Extraer los mismos datos pero iterando por todas las paginas