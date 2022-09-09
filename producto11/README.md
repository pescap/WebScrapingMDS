Integrantes : 
GeorgeAdrock
LitzyCastro
enriques76

##  El proyecto o Idea de WebScrapping.
Este repositorio contiene:
README.md: Nombre de proyecto y descripción corta del proyecto
users.txt:logins de los integrantes del grupo
requirements.txt: Librerías que se usan para el proyecto
scraper.py: código fuente del scraper
plot.py: Análisis de datos, plots


# BolsaTrabajo_CienciaDatos
 Estadistica y recopilacion de informacion de ofertas de trabajo relacionadas con Data Science

##  El proyecto o Idea de WebScrapping.
Se pretende comenzar con un analisis sobre la bolsa de trabajo publicados en Linkedin, para los roles asociados a la Ciencia de Datos en Chile.

Este repositorio contiene:
README.md: Nombre de proyecto y descripción corta del proyecto
users.txt:logins de los integrantes del grupo
requirements.txt: Librerías que se usan para el proyecto
scraper.py: código fuente del scraper
plot.py: Análisis de datos, plots


# BolsaTrabajo_CienciaDatos
 Estadistica y recopilacion de informacion de ofertas de trabajo relacionadas con Data Science

##  El proyecto o Idea de WebScrapping.
Se pretende comenzar con un analisis sobre la bolsa de trabajo publicados en Linkedin, para los roles asociados a la Ciencia de Datos en Chile.

Se construye un DataFrame con la informacion obtenida del scrapeo de la pagina. 
Se busca tabular informacion relacionada con skill asociados a:
- Lenguaje de programcion
- Base de datos
- uso de Nubes
- Herramientas

etc.

Los pasos definidos a seguir son:

1. A través de la libreria Selenium, navegar sobre el sitio de linkedin y obtener la lista de ofertas cada 24 horas. Alamacenaremos el link de cada página en un data frame.

2. Leer el dataframe con direcciones de las paginas y avisos que se escrapeará, para posteriomente rescatar los datos de interés. Para este paso, utilizaremos la libreria Beautiful Soup.

3. Visualizar  y realizar un análisis de la información respecto de la data obtenida, utilizando librerias de python como plotly.