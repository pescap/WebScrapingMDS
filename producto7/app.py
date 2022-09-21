import streamlit as st
import pandas as pd
import requests
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd
import io
import streamlit as st
import plotly.express as px
import numpy as np

def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_data_cs(url):
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text) ) if response.ok else None
    return df


def show_df_agrid(data):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        height=500, 
        width='60%',
        reload_data=True
    )
    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

def plot_data(data):

    data_grouped = (
        data[data['Sala'].isin(['PRIMERA','SEGUNDA','TERCERA','CUARTA'])][['Sala', 'Causa1', 'Causa2', 'Causa3', 'Causa4']]
        .reset_index(drop=True)
        .set_index('Sala')
        .stack()
        .groupby(level=[0,1])
        .value_counts()
        .unstack(1, fill_value=0)
        .reset_index()
        .rename(columns={'level_1':'Causa'})
    )
    data_grouped['Cantidad'] = data_grouped['Causa1'] + data_grouped['Causa2'] + data_grouped['Causa3']
    fig = px.bar(data_grouped, x="Causa", y="Cantidad", color="Causa", barmode="group", facet_col="Sala")
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.sidebar.markdown("# WebScraping Corte Suprema")
    st.sidebar.write("Información de integración de las salas de la corte suprema y los motivos de inasistencia ante ausencia de ministros.")
    st.sidebar.markdown("---")
    periodo = st.sidebar.radio(
        "Seleccione el periodo de los registros a consultar",
        ("2022", "2020-2021", "2018-2019","2015-2017")
    )
    url_base = "https://raw.githubusercontent.com/jwilenmann/WebScraping-Cs/main/Scraper/output/"
    if periodo == "2015-2017":
        url = url_base + "20222808_2015_2017.csv.csv"
    elif periodo == "2018-2019":
        url = url_base + "20220830_2018_2019.csv.csv"
    elif periodo == "2020-2021":
        url = url_base + "20222108_2020_2021.csv.csv"
    else:
        url = url_base + "2022_01_08.csv.csv" 

    st.markdown(f"## Datos del periodo {periodo}")
    data = get_data_cs(url)
    if "Unnamed: 0" in data.columns:
        data = data.drop(columns="Unnamed: 0")
    if periodo != "2020-2021":
        plot_data(data)
    show_df_agrid(data)
    df_xlsx = to_excel(data)
    st.download_button(label='📥 Descargar resultados',data=df_xlsx ,file_name= f"datos_inasistencias_y_causa_{periodo}.xlsx")

if __name__=='__main__':
    main()
