# Scraper sitio https://www.spensiones.cl/


Proyecto permite extraer los valores cuotas y patrimonio que administra cada AFP de Chile. La información es obtenida desde la superintendencia de pensiones.

Existen 5 fondos de ahorros para las pensiones chilenas, el más riesgoso es el fondo A y el más conservador es el fondo E. 

Fondos administrados por las AFP: A, B, C, D, E.

Las AFP que se encuentran dentro del análisis son todas las que existen en Chile, son reguladas financieramente por la CMF y la superintendencia de AFP.

- CAPITAL
- CUPRUM
- HABITAT
- MODELO
- PLANVITAL
- PROVIDA
- UNO

Los datos que se descargan son los valores cuotas y patrimonio diario por cada fondo y por cada AFP del país.


# Aplicaciones con los datos del proyecto:

Con esta data se podría usar para validar las cartolas de nuestros ahorros que se encuentran en la AFP, ya que lo informado a la superintendencia debería ser lo mismo que tiene nuestra cartola personal de ahorro.

Esta información es útil para los operadores del mercado financiero, ya que los movimientos de cambios patrimoniales entre fondos en ciertos periodos genera mucha volatilidad y existen cambios masivos de personas que están en el fondo A (fondo riesgoso) por ejemplo pasan al fondo E (mas conservado). Estos movimientos de cambios de las personas, hacen que los instrumentos de renta fija y renta variable tengan alta volatilidad en sus precios por la alta demanda de vender o comprar papeles financieros.

docs:
- Scraping Superintendencia de Pensiones.pdf: Se encuentra presentación del proyecto

Toda la información que se descarga se almacena en la 📂 "output"

Los archivos que se tienen son 5 csv uno por cada fondo administrado con la información diaria de valores cuotas y patrimonio de cada AFP en pesos chilenos. Los archivos contienen la información de todo el 2022, es decir, todos los días se podrá actualizar la descarga y se tendrá el archivo del año actual con todos los valores actualizados para cada día. Por lo tanto, la carpeta tendrá solo los 5 csv diariamente con la información de cada fondo (A, B, C, D, E).


