# Proyecto: Scraping de Noticias Financieras

## Contexto
El siguiente producto busca poder generar una base de datos historicas de noticias financieras relacionadas a instrumentos, con el objetivo de ser utilizada posteriormente como insumos a modelos de prediccion, combinando Procesamiento de Lenguaje Natural con otros Algoritmnos para apoyar a la hora de tomar decisiones de compra y venta de acciones. 

Se busca generar distintas estrucutras de CSV 

## Pasos a seguir

Se obtendra titulares e informacion de distintos portales financieros:

- Yahoo! Finance: https://finance.yahoo.com/
- Financial Times: https://www.ft.com/
- Investing: https://www.investing.com/
- FinViz: https://finviz.com/

Se crearan distintos CSV con distintas estructuras como propuestas para resolver el problema de clasificacion de compra/no compra. 


IMPORTANTE: para la propuesta 3 de juntar datos de FinViz e Investing, solo se concreta para este curso la generacion de datos con FinViz. En un futuro se utilizara una API de Yahoo Finance para obtener datos historicos de acciones y se utilizara finviz y FT para obtener ojala al menos 25 titulares por instruemnto por dia

## Este repositorio contiene:

- Jupyter Notebook "A_yahooFinance", el cual contiene el scraping y NLP para Yahoo! Finance
- Script "B_financialTimes", scraping del Financial Times
- Script  "C_finviz", scraping de portal FinViz
- Script  "C_investing", scraping en revision del portal Investing
- "requirements.txt", el cual contiene el detalle de las librerias utilizadas y sus versiones
- "users.txt" el cual detalla los usuarios de GitHub de los integrantes del grupo 
docs:
- 

