import pandas as pd
import time
import os
import tabula
import re
import PyPDF2
import locale
import io
import glob
import sys
import gc


os.environ['w2n.lang'] = 'es'


columns = ['Fecha', 'Sala', 'Integrantes', 'Causa']
df = pd.DataFrame(columns = columns)

palabras = ['licencia', 'comisi ón', 'permiso', 'feriado', 'inhabilidad', 'subroga', 'vacancia']


pdf_files = glob.glob(os.path.join(os.getcwd(), "output",'*.pdf'))

count = 0
extractedtext = ""
for pdf_file in pdf_files:
    print(pdf_file)
    pdfFileObj = open(pdf_file,'rb')               
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   
    num_pages = pdfReader.numPages
    pdfPageObj = pdfReader.getPage(0)
    text = pdfPageObj.extractText()
    Causa = []
    if re.search("INSTALACI", text):
        Integrantes = re.findall('(?<=ÑOR).*?(?=\s)', text)
        try:
            Fecha = re.findall('(?<=FIRMADIGITAL).*?(?=\\\n)', text)[0]
        except:
            pass
        try:
            Sala = re.findall('(?<=\\s).*?(?=\\sSALA)', text)[0]
        except:
            pass
        for palabra in palabras:         
            if palabra in text:
                Causa.append(palabra)
        df = df.append(
               {"Fecha" : str(Fecha), "Sala" : str(Sala), "Integrantes" : Integrantes, 'Causa' : Causa},
               ignore_index=True,
            )

df['Fecha'] = df['Fecha'].str.replace("treinta y uno", "treintaiuno")
df['Dia'] = df['Fecha'].str.split(' ').str[0] 
df["Ano"] = df["Fecha"].str.extract(r'(\w+)$')
df['Dia'] = df['Dia'].str.replace("treintaiuno", "treinta y uno")

nums = {'^uno$': '1', '^dos$': '2', '^tres$': '3', "^cuatro$":'4', "^cinco$" : '5', "^seis$":'6', "^siete$": '7', 
        '^ocho$':'8',
       '^nueve$':'9', 'diez':'10', 'once':'11', 'doce':'12', 'trece':'13','catorce':'14', 'quince': '15', 'dieciséis':'16',
        'diecisiete':'17', 'dieciocho':'18', 'diecinueve':'19', 'veinte':'20', 'veintiuno':'21','veintidós':'22', 
        'veintitrés':'23', 'veinticuatro':'24', 'veinticinco':'25', 'veintiséis':'26', 'veintisiete':'27',
        'veintiocho':'28', 'veintinueve': '29', '^treinta$': '30', 'treinta y uno': '31'}
        

for old, new in nums.items():
    df['Dia'] = df['Dia'].str.replace(old, new, regex=True)

nums = {'^veinte$': '20', '^veintiuno$': '21', '^veintidós$': '22'}
        

for old, new in nums.items():
    df['Ano'] = df['Ano'].str.replace(old, new, regex=True)

df['Ano'] = df['Ano'].astype(str)
df['Dia'] = df['Dia'].astype(str)#aisla y convierte a una columna mes
df["Mes"] = df["Fecha"]
df['Mes'] = df['Mes'].str.split(n=1).str[1]
df['Mes'] = df['Mes'].str.lstrip()
df['Mes'] = df['Mes'].str.split(' ').str[1] 

meses = {'enero': '01', 'febrero': '02', 'marzo': '03', "abril":'04', "mayo" : '05', "junio":'06', "julio": '07', 
        'agosto':'08', 'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'}
        

for old, new in meses.items():
    df['Mes'] = df['Mes'].str.replace(old, new, regex=True)

#concatenación fecha en formato
df['Fecha2'] = df['Dia'] + '/' + df['Mes'] + '/' + df['Ano']
#transformación a datetime
df['Fecha2'] = pd.to_datetime(df["Fecha2"], format = '%d/%m/%y')

df2 = df
df2['Presidente'] = df2['Integrantes'].str[0]
df2['Integrante1'] = df2['Integrantes'].str[1]
df2['Integrante2'] = df2['Integrantes'].str[2]
df2['Integrante3'] = df2['Integrantes'].str[3]
df2['Integrante4'] = df2['Integrantes'].str[4]

df3 = df2
df3 = df3.drop(['Fecha', 'Integrantes', 'Dia', 'Ano', 'Mes'], axis = 1)


df3['Causa1'] = df3['Causa'].str[0]
df3['Causa2'] = df3['Causa'].str[1]
df3['Causa3'] = df3['Causa'].str[2]
df3['Causa4'] = df3['Causa'].str[3]


df3 = df3.drop(['Causa'], axis = 1)

df3.drop_duplicates()

df3.to_csv("2022_08.csv")
