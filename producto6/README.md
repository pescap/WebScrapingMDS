Se busca que el proyecto integre todas las tecnologías vistas en clase, para lo cual, desarrollaremos un script que pueda:
1. Revisar si existe la carpeta output, en caso de no existir, la crearemos.

2. Navegar la página de Investing (https://www.investing.com/equities/falabella) con Selenium.
  • Realizar todas las interacciones necesarias vía navegador para que la página web genere la información que necesitamos.

3. Integrar el código fuente obtenido de la interacción de Selenium con Beautiful Soup 4 para poder descargar la información.
4. Dar formato la información descargada:
  • Convertir la información a DF.
  • Limpiar y ajustar el formato del DF.
  • Exportar a csv.

Este repositorio contiene:

README.md: Nombre de proyecto y descripción corta del proyecto -- Este Archivo

users.txt:logins de los integrantes del grupo

scraper.py: código fuente del scraper

docs.pdf: los slides de la presentacion

requirements.tx: agregar las librerías que se usan para el proyecto

output:

Falabella.xlsx
