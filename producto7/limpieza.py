import pandas as pd
import os
import re
import PyPDF2
import glob
from datetime import date


os.environ['w2n.lang'] = 'es'


def extractor(list_palabras, dir_input):
    """Funcion que extrae informacion de conformacion de las salas y causas de inasistencia y las restorna en un dataframe"""
    pdf_files = glob.glob(dir_input)
    list_registros = []

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
            for palabra in list_palabras:         
                if palabra in text:
                    Causa.append(palabra)
            list_registros.append(
                {"Fecha" : str(Fecha), "Sala" : str(Sala), "Integrantes" : Integrantes, 'Causa' : Causa}
                )
    df = pd.DataFrame.from_dict(list_registros)
    return df

def clean_df(df):
    """Funcion que limpia dataframe segun su contenido"""
    df['Fecha'] = df['Fecha'].str.replace("treinta y uno", "treintaiuno")
    df['Dia'] = df['Fecha'].str.split(' ').str[0] 
    df["Anio"] = df["Fecha"].str.extract(r'(\w+)$')
    df['Dia'] = df['Dia'].str.replace("treintaiuno", "treinta y uno")

    nums = {'^uno$': '1', '^dos$': '2', '^tres$': '3', "^cuatro$":'4', "^cinco$" : '5', "^seis$":'6', "^siete$": '7', '^ocho$':'8',
            '^nueve$':'9', 'diez':'10', 'once':'11', 'doce':'12', 'trece':'13','catorce':'14', 'quince': '15', 'dieciséis':'16',
            'diecisiete':'17', 'dieciocho':'18', 'diecinueve':'19', 'veinte':'20', 'veintiuno':'21','veintidós':'22', 'veintitrés':'23',
            'veinticuatro':'24', 'veinticinco':'25', 'veintiséis':'26', 'veintisiete':'27', 'veintiocho':'28', 'veintinueve': '29', '^treinta$': '30', 'treinta y uno': '31'}      

    for old, new in nums.items():
        df['Dia'] = df['Dia'].str.replace(old, new, regex=True)

    nums = {'^veinte$': '20', '^veintiuno$': '21', '^veintidós$': '22'}
            

    for old, new in nums.items():
        df['Anio'] = df['Anio'].str.replace(old, new, regex=True)

    df['Anio'] = df['Anio'].astype(str)
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
    df['Fecha2'] = df['Dia'] + '/' + df['Mes'] + '/' + df['Anio']
    #transformación a datetime
    df['Fecha2'] = pd.to_datetime(df["Fecha2"], format = '%d/%m/%y')

    # desintegracion de integrantes y causas 
    df['Presidente'] = df['Integrantes'].str[0]
    for i in range(1,5):
        df[f'Integrante{i}'] = df['Integrantes'].str[i]
    for i in range(1,5):
        df[f'Causa{i}'] = df['Causa'].str[i]
    
    df.drop(['Fecha', 'Integrantes', 'Causa', 'Dia', 'Anio', 'Mes'], axis=1, inplace=True)
    df.drop_duplicates(inplace = True)

    return df


def clean_directory(dir_output):
    """Funcion que elimina todos los archivos de tipo pdf de la carpeta de output"""
    os.chdir(dir_output)
    files=glob.glob('*.pdf')
    for filename in files:
        try: 
            os.unlink(filename)
        except:
            pass


def main():
    list_palabras = ['licencia', 'comisi ón', 'permiso', 'feriado', 'inhabilidad', 'subroga', 'vacancia']
    base_dir = os.path.join(os.getcwd(), "output")
    dir_input = os.path.join(base_dir,'*.pdf')

    # Extraccion y limpieza
    df = extractor(list_palabras, dir_input)
    df_clean = clean_df(df)

    # Guardado de resultados
    dir_output = os.path.join(base_dir, f"resultados_scraper_{date.today()}.csv")
    df_clean.to_csv(dir_output, index=False, encoding='utf-8-sig')

    # Limpieza de pdfs en el directorio
    clean_directory(base_dir)


if __name__ == "__main__":
    main()
