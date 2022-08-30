## Importamos las librerias necesarias para generar el scraper
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
import os
import re

## Datos básicos para hacer el request (url, headers)
url = "https://aplicativos.odepa.gob.cl/avancemensual.do"
headers = {
  'Cookie': 'JSESSIONID=2E9275A55DAFA54F9AFEE077EA378990'
}
page = rq.request("GET", url, headers=headers)

## Se define una función para obtener los parámetros de cada elemento del formulario
def get_element(lista):
    limpio = []
    for x in lista:
        limpio.append([x['value'], x.text])
    return limpio

## Generación del diccinario con los parámetros del formulario
# De la revisión del html sabemos que los 'id' de los 'select' de los campos necesarios para el scraper son:
campos = {'mesini':'cboMesIni', 
'anioini':'cboAgnoIni', 
'mesfin':'cboMesFin', 
'aniofin':'cboAgnoFin',
'producto':'cboProducto',
'region':'cboRegion'
}

# Se hace el request para obtener los parámetros del formulario y se guardan en el diccionario 'parametros'
parametros = {}
soup = bs(page.content, 'html.parser')
for key, value in campos.items():
    temp = soup.find('select', attrs={'id':value})
    valor = get_element(temp.find_all('option'))
    parametros[key] = valor

## Se hace una serie de request del tipo POST para obtener los datos mensuales de cada año, de cada producto y de cada región.
# Se hace una lista con los años que se van a scrapear, otra con los productos y otra con las regiones
anios = [min(parametros['anioini']), max(parametros['aniofin'])]
productos = parametros['producto']
regiones = parametros['region'][1:]

## Ciclos para recorrer todos los parámetros y hacer los request
# dataframe vacío para guardar los datos
dffinal = pd.DataFrame()
# Ciclos
for producto in productos:
    for region in regiones:

        # Payload para entregarlo al POST request
        payload = {'dataExport': '',
        'compressed': 'false',
        'fileNameExcel':'',
        'decimales':'',
        'cboMesIni': '01',
        'cboAgnoIni': anios[0][0],
        'cboMesFin': '06',
        'cboAgnoFin': anios[1][0],
        'cboProducto': producto[0],
        'rdoTipo': 'region',
        'cboRegion': region[0],
        'rdoFormatoTabla': 'mesagno'}

        # Se hace el request
        page = rq.request("POST", url, headers=headers, data=payload)

        # Solo consideramos los resultados que no estén vacíos
        if page.status_code == 200:
            # Se obtiene el html de la página y se parsea con BeautifulSoup
            soup = bs(page.text, 'html.parser')
            columns = []
            data = []
            table = soup.find('table', attrs={'class':'tbl_informe'})
            table_body = table.find('tbody')
            table_head = table.find('thead')
            fields = table_head.find_all('th')
            rows = table_body.find_all('tr')

            # Dado que los datos se encuentran en una tabla, se recorren los títulos y el cuerpo
            for field in fields:
                columns.append(field.text)
                
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values

            # Se guardan los datos en un dataframe
            tabla = pd.DataFrame(data, columns=columns)

            # Se eliminan los datos que no sean necesarios (última columna y última fila)
            tabla.drop(tabla.columns[-1], axis=1, inplace=True)
            tabla = tabla.loc[:len(tabla)-2]

            # Se agrega el producto y la región a los datos para saber a que corresponde cada tabla
            tabla['Producto'] = producto[1]
            tabla['Region'] = region[1]

            # Se agrega la tabla al dataframe final
            dffinal = pd.concat([dffinal, tabla])


## Normalizamos los datos para que sean más legibles por software de análisis
dffinal = pd.melt(dffinal, id_vars=['Meses','Producto', 'Region'], value_vars=dffinal.columns[1:-2], value_name='Valor')
dffinal.rename(columns={'variable': 'Año'}, inplace=True)

## Los datos de la columna valor son tipo object, por lo que deben ser convertidos a valores de tipo int
for i in range(len(dffinal)-1):
    dffinal['Valor'][i] = int(re.sub(r'\W','',dffinal['Valor'][i]))

dffinal['Valor'] = dffinal['Valor'].astype(int)

## Se almacena en un csv
cwd = os.getcwd()
dffinal.to_csv(cwd+'\\output\\df_final.csv', index=False)

