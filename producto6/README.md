Se busca que el proyecto integre todas las tecnologías vistas en clase, para lo cual, desarrollaremos un script que pueda:
1. Navegar la página de la bolsa de Santiago (https://www.investing.com/equities/falabella) con Selenium.
• Todo esto con iteradores y listas para consultar un número controlado de empresas.

2. Descargar información que se refleje en la página, con Beautiful Soup 4

3. Sobre las lógicas:

• Idealmente si la Empresa es “nueva” en el proceso de consultas, deberemos crear una carpeta con Selenium y/o OS (Siempre y
cuando exista dentro del consultador la bolsa de Santiago.
• De lo contrario, deberá leerse la carpeta respectiva con los archivos descargados anteriormente.
• Los puntos a y b de este apartado deberán ser controlados y manipulados con Pandas

Este repositorio contiene:

README.md: Nombre de proyecto y descripción corta del proyecto -- Este Archivo
users.txt:logins de los integrantes del grupo

scraper.py: código fuente del scraper
docs.pdf: los slides de la pre-presentación (y luego presentación final)
output:

Falabella.xlsx

Pendiente:

requirements.tx: agregar las librerías que se usan para el proyecto

plot.py: opcional: sirve si quieren agregar un análisis de datos, unos plots
docs:

Guardar acá los resultados del scraper en formato .csv (recomendado) o .xlsx