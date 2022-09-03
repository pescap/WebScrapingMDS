# Proyecto Grupo Producto 8
## Web Scraping de Departamentos

Se busca desarrollar un scraper que trabaje sobre el sitio web 
de portalinmobiliario.com para armar una base de datos de 
inmuebles en arriendo a fin de poder observar la variación de 
los precios de arriendo en el tiempo, para así identificar la 
mejor alternativa en términos de calidad / precio.

Con este scraper se obtendrán los datos de departamentos disponibles para arriendo de acuerdo a:
- Ubicación geográfica
- Cantidad de dormitorios
- Estacionamiento
Para el alcance del proyecto, se define la “mejor alternativa” aquella que se encuentre dentro de los barrios de interés, posea dos dormitorios y a su vez:
- Mínimo precio
- Máxima superficie
 
## Herramientas 

Dada la naturaleza dinámica del sitio web, se proyecta utilizar Selenium tanto para entregar al sitio web los filtros correspondientes como para navegar entre las páginas de resultados y obtener los datos asociados a cada oferta de arriendo.
Algunos puntos relevantes con respecto a la infraestructura del sitio web y que fundamentan la elección de usar Selenium son:
- No cuenta con una API
- No requiere de log in para buscar la información de arriendos
- No contiene captchas de validación de identidad
- No presenta mayores restricciones de conexión

##  Pasos a realizar

1. Acceder al sitio web de portal inmobiliario
2. Ingresar los filtros de:  
    a. Barrios de Interés.   
    b. Valos máximo de arriendo.  
    c. Cantidad mínima de habitaciones. 
3. Ordenar los resultados por menor precio
