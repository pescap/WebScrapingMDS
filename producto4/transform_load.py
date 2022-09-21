#!/usr/bin/env python
# coding: utf-8

# In[33]:


import os
import pandas as pd


# In[44]:


# Carpeta con la data
path = "./output"

# extension a detectar
extension = '.csv'
li = []

for root, dirs_list, files_list in os.walk(path):
    for file_name in files_list:
        if os.path.splitext(file_name)[-1] == extension:
            file_name_path = os.path.join(root, file_name)
            #print(file_name)
            #print(file_name_path)
            #print(pd.read_csv(file_name_path).head())
            df = pd.read_csv(file_name_path, index_col=None, header=0)
            li.append(df)

            
salida = pd.concat(li, axis=0, ignore_index=True)

nombre_archivo = '_full_' + '.csv' 
csv_folder = 'output/'
file_dir = os.path.dirname(os.path.abspath("__file__"))


file_path = os.path.join(file_dir, csv_folder, nombre_archivo)
salida.to_csv(file_path, index=False)
print('Archivo guardado', nombre_archivo)
print("")

