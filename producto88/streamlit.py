# Importamos las librerias necesarias
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os
import math
import datetime as dt
import plotly.express as px

# Secciones
header = st.container()
metricas = st.container()
chart_productos = st.container()


# lectura de datos
cwd = os.getcwd()
archivo = Path(__file__).parents[0] / 'output/df_final.csv'
dffinal = pd.read_csv(archivo)

#Header
with header:
    st.title('Productos lácteos en Chile')
    st.write('''
Actualmente Chile es un país sumamente dependiente de otras naciones respecto de sus necesidades alimenticias. Esto se traduce en una debilidad para la economía pues frente a situaciones como la guerra en Ucrania o desastres naturales, se generan variaciones de precio debido a la escasez. Frente a esta situación nos hemos enfocado en analizar la situación productiva chilena en alimentos lácteos, con la finalidad de conocer si esta actividad productiva tiene una tendencia positiva o negativa, y establecer un panel de control que permita monitorear estos comportamientos.
Con lo anterior queremos visibilizar esta situación dejando el análisis en un plataforma abierta para que cualquier ciudadano pueda conocer esta información en visualizaciones de rápido entendimiento
''')
st.write(f'\n')

## Calculos para las métricas
# funcion para obtener el último mes con datos
def ultimo_mes(df, anio):
    a = df.loc[(df['Año']==anio)].groupby(['Meses'])['Valor'].sum().reset_index()
    mes = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, \
        'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}
    a['mesn'] = a.Meses.map(mes)
    a.sort_values(by=['mesn'], inplace=True)
    a.reset_index(drop=True, inplace=True)
    ult_mes = max(a.loc[a['Valor']!=0]['mesn'])
    final = a.loc[ult_mes-2:ult_mes-1][['Meses', 'mesn']]
    return final.reset_index(drop=True)

# Variables descriptivas
anio = dt.date.today().year
meses = ultimo_mes(dffinal,anio)
ultimo = str.lower(meses['Meses'].values[1])
penultimo = str.lower(meses['Meses'].values[0])

# Sección métricas
with metricas:
    st.write(f'## Métricas de {ultimo}')
    st.write(f'A continuación se presentan las cantidades producidas a nivel Nacional de cada producto durante el mes de {ultimo} de {anio}, junto a esto se encuentra la variación porcentual respecto a {penultimo}')
    st.write('\n')
    st.write('\n')

    ##  Código para imprimir cada una de las métricas por producto
    filas = math.ceil(len(dffinal['Producto'].unique())/3)
    # Ciclo para recorrer cada fila de 3 columnas
    for j in range(filas):
        cols = st.columns(3)
        for i in range(3):
            # Condición para evitar errores
            if j*3+i < len(dffinal['Producto'].unique()):
                
                # Se obtienen los parámetros necesarios para imprimir como métricas
                temp = dffinal.loc[(dffinal['Producto']==dffinal['Producto'].unique()[j*3+i])&(dffinal['Año']==anio)&(dffinal['Meses'].isin(meses['Meses'].values))]
                temp = temp.groupby(['Producto', 'Meses'])['Valor'].sum().reset_index()
                mes_actual = temp.loc[temp['Meses']==meses['Meses'][1]]['Meses'].values[0]
                mes_anterior = temp.loc[temp['Meses']==meses['Meses'][1]]['Meses'].values[0]
                produccion = temp.loc[temp['Meses']==meses['Meses'][1]]['Valor'].values[0]
                if temp.loc[temp['Meses']==meses['Meses'][0]]['Valor'].values[0] != 0:
                    diff = round((temp.loc[temp['Meses']==meses['Meses'][1]]['Valor'].values[0] - temp.loc[temp['Meses']==meses['Meses'][0]]['Valor'].values[0])/(temp.loc[temp['Meses']==meses['Meses'][0]]['Valor'].values[0]) * 100)
                else:
                    diff = 0
                producto = dffinal['Producto'].unique()[j*3+i]
                produccion = '{:,}'.format(produccion).replace(',','.')

                # Se imprimen las métricas
                cols[i].metric(producto, produccion, str(diff) + '%')

#Sección regiones
with chart_productos:
    st.write('\n \n \n \n')
    st.write('## Análisis evolutivo de la producción mensual por producto')
    st.write('A continuación se presenta un gráfico evolutivo interactivo, en el se puede ver como ha ido cambiando a través del tiempo la cantidad que se produce en cada región respecto de cada producto')

    # Selector
    option = st.selectbox(
     'Seleccione el prodcuto a mostrar en el gráfico',
     (dffinal['Producto'].unique()))

    st.write('Evolución de la producción de ', option)

    # Creación de dataset usado para el gráfico
    dfproducto = dffinal.loc[dffinal['Producto']==option]
    dfproducto['año-mes'] = dfproducto['Año'].astype('str') + ' - ' + dfproducto['Meses']

    # Gráfico usando la librería plotly
    fig = px.line(dfproducto, x="año-mes", y="Valor", color='Region')
    fig.for_each_xaxis(lambda x: x.update(showgrid=False))
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)
    