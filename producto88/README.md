# Proyecto: Webscraping de producción mensual de productos lácteos en Chile

## Contexto

Actualmente Chile es un país sumamente dependiente de otras naciones respecto de sus necesidades alimenticias. Esto genera se traduce en una debilidad para la economía pues frente a situaciones como la guerra en Ucrania o desastres naturales, se generan enormes variaciones de precio debido a la escasez. Frente a esta situación nos hemos enfocado en analizar la situación productiva chilena en alimentos lácteos, con la finalidad de conocer si esta actividad productiva tiene una tendencia positiva o negativa, y establecer un panel de control que permita monitorear estos comportamientos.
Con lo anterior queremos visibilizar esta situación dejando el análisis en un plataforma abierta para que cualquier ciudadano pueda conocer esta información en visualizaciones de rápido entendimiento

## Pasos a seguir

Analizar la web https://www.odepa.gob.cl/avance-mensual-y-series-de-tiempo-de-productos-por-planta-o-region-de-la-industria-lactea 
Crear un scraper que extraiga la la información necesaria.
Almacenar los datos en archivos csv.
Generar visualizaciones públicas de actualización mensual usando streamlit.

## Este repositorio contiene:

- README.md: Nombre de proyecto y descripción corta del proyecto
- users.txt:logins de los integrantes del grupo
- requirements.tx: agregar las librerías que se usan para el proyecto
- scraper.py: código fuente del scraper
- plot.py: opcional: sirve si quieren agregar un análisis de datos, unos plots
- streamlit.py: código para levantar una aplicación gráfica en la plataforma cloud Streamlit
  
docs:
- docs.pdf: los slides de la pre-presentación (y luego presentación final)

output:

Los resultados del scraper en formato .csv

## Resultados

Para ver los resultados del scraper convertido en una panel de visualización haz clic en este [enlace en línea](https://josemoragonzalez-webscrapingmds-producto88streamlit-t3mflb.streamlitapp.com/)