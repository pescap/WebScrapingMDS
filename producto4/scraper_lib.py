import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import os
from datetime import date, timedelta
import re


class Sismo:
    pass

def get_data(s):   
    sismos = []
    for i in s:
        if i.find("th", class_="icon-search") is not None:
            #print("buscador")
            next
        elif (i.find("th", text=re.compile(".*Fecha Local / Lugar.*")) is not None):
            #print("header")
            next
        else:
            
            sismo = Sismo()
            sismo.evento = i.find_all('td')[0].text[19:] #Lugar
            sismo.fecha_local = i.find_all('td')[0].text[:19] #Lugar
            sismo.fecha_utc = i.find_all('td')[1].text # Fecha
            sismo.lat = "-" +  i.find_all('td')[2].text.split("-")[1] #Latitud
            sismo.lng = "-" +  i.find_all('td')[2].text.split("-")[2] # Longitud
            sismo.profundidad = i.find_all('td')[3].text # Profundidad
            sismo.magnitud = i.find_all('td')[4].text #Magnitud 
            sismos.append(sismo)
    return pd.DataFrame.from_records([t.__dict__ for t in sismos ])

def get_source(fecha):
    fecha_data = pd.to_datetime(fecha)
    url = 'https://www.sismologia.cl/sismicidad/catalogo/'+fecha_data.strftime('%Y/%m/%Y%m%d')+'.html'
    print("Ruta_log: ",url)
    ssm = requests.get(url)
    s = BeautifulSoup(ssm.text, 'html.parser').find_all('tr')
    return s

def process_data(df):
    df[["fecha_local", "hora_local"]] = df["fecha_local"].str.split(' ', expand=True)
    df[["fecha_utc", "hora_utc"]] = df["fecha_utc"].str.split(' ', expand=True)
    df[["profundidad", "profundidad_unidad"]] = df["profundidad"].str.split(' ', expand=True)
    df[["magnitud", "magnitud_unidad"]] = df["magnitud"].str.split(' ', expand=True)
    
    return df[['evento', 'lat', 'lng', 'fecha_local', 'hora_local', 
            'fecha_utc', 'hora_utc', 'profundidad', 'profundidad_unidad','magnitud','magnitud_unidad']]

def get_today_as_string():
    return date.today().strftime("%m/%d/%Y")

def get_yesterday_as_string():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime("%m/%d/%Y")

def save_file(df, fecha):
    fecha_data = pd.to_datetime(fecha)
    nombre_archivo = fecha_data.strftime('%Y%m%d') + '_sismos_' + '.csv' 
    file_dir = os.path.dirname(os.path.abspath("__file__"))
    csv_folder = 'output/' + fecha_data.strftime('%Y') + "/" + fecha_data.strftime('%m')
    try:
        os.makedirs(os.path.join(file_dir, csv_folder))
    except FileExistsError:
        pass
    file_path = os.path.join(file_dir, csv_folder, nombre_archivo)
    df.to_csv(file_path, index=False)
    print('Archivo guardado', nombre_archivo)
    print("")
    
    
def process_yesterday():
    #Obtenemos la fecha del día anterior
    yesterday = get_yesterday_as_string()

    #Obtenemos los datos de nuestro sitio
    fuente = get_source(yesterday)

    #Obtenemos los datos en formato dataframe
    df_sismos = get_data(fuente)

    #Procesar datos
    df_sismos = process_data(df_sismos)

    #Guardamos nuestros datos en formato csv
    save_file(df_sismos, yesterday)
    

def process_history(date):
    #Obtenemos los datos de nuestro sitio
    fuente = get_source(date)

    #Obtenemos los datos en formato dataframe
    df_sismos = get_data(fuente)

    #Procesar datos
    df_sismos = process_data(df_sismos)

    #Guardamos nuestros datos en formato csv
    save_file(df_sismos, date)
    
def create_process_history(fecha_inicio, sleep_time = 2):
    
    #la historia se mide hasta 2 días atras, el día anterior es parte del scraping diario
    fecha_termino = (date.today() - timedelta(days=2)).strftime("%m/%d/%Y") 

    rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_termino)

    for fecha in rango_fechas:
        process_history(fecha.strftime("%m/%d/%Y"))
        sleep(sleep_time)
        
