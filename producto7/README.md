# WebScraping-CS

### Scraping Corte Suprema
Proyecto para el curso de WebScraping consistente en la obtención automática de información de integraciones de la Corte Suprema desde el año 2014.

El proyecto funciona sobre la base de Selenium y la extracción de información de PDFs escaneados y no escaneados. 

Se puede visualizar la data desde la siguiente app disponible en https://scraping-cs-eoakmwhgya-uc.a.run.app 

La app fue hecha con streamlit y deployada en un cloud run de Google Cloud Platform y consume los datos que se guardan en la carpeta output del presente repositorio.

El archivo scraper.py contiene el script para bajar los PDFs, mientras que el archivo limpieza.py contiene el script que extrae la informacion de los pdfs descargados y la guarda en un csv dentro de la carpeta output.


