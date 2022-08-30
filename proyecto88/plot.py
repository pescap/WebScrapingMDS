# %%
## Importamos las librerias necesarias

import pandas as pd
import seaborn as sns
import os
import numpy as np
import matplotlib.pyplot as plt

# %%
## Se definen las características generales de los gráficos

plt.rcParams['figure.figsize'] = 15,8
sns.set(style='whitegrid')

# %%
## Se lee el archivo csv

cwd = os.getcwd()
dffinal = pd.read_csv(cwd+'/output/df_final.csv')
dffinal.head()

# %%
## Se procesan los datos para generar una columna de fechas que nos permita generar series de tiempo

meses_dicc = {'Enero': 1,
              'Febrero': 2,
              'Marzo': 3,
              'Abril': 4,
              'Mayo': 5,
              'Junio': 6,
              'Julio': 7,
              'Agosto': 8,
              'Septiembre': 9,
              'Octubre': 10,
              'Noviembre': 11,
              'Diciembre': 12}

# %%
dffinal['Mes']=np.nan
for i in np.arange(len(dffinal)):
    dffinal['Mes'][i]=int(meses_dicc[dffinal['Meses'][i]])

dffinal['Mes'] = dffinal['Mes'].astype(int)
dffinal['Dia'] = 1
cols = ['Año', 'Mes', 'Dia']
dffinal['Fecha'] = dffinal[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
dffinal['Fecha'] = pd.to_datetime(dffinal['Fecha'])

# %%
## Se genera un gráfico para cada región

regiones = dffinal['Region'].unique()
for i in range(len(regiones)):
    productos = dffinal['Producto'][dffinal['Region']==regiones[i]].unique()
    legenda = []
    for producto in productos:
        filtro = (dffinal['Producto']==producto) & \
                (dffinal['Region']==regiones[i])
        df_filter = dffinal[['Fecha','Valor']][filtro]
        if df_filter['Valor'].sum()>0: # solo se grafica si el producto presenta una sumatoria mayor a cero
            legenda.append(producto)
            sns.lineplot(data = df_filter, x ='Fecha', y = 'Valor')
    plt.legend(legenda)
    plt.title(f'Producción Láctea Región {regiones[i]}', fontsize=15)
    plt.savefig(cwd+f'/output/{i}-{regiones[i]}.png')
    plt.clf()
    #plt.show()



