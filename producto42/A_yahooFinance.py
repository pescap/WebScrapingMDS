
from shelve import DbfilenameShelf
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
from pandas import Series, DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile
from bs4 import BeautifulSoup
from textblob import TextBlob
import textblob
import csv

driver = webdriver.Chrome()

link = 'https://finance.yahoo.com/topic/stock-market-news/'
driver.get(link)
driver.maximize_window()

for i in range(1,15):
    driver.execute_script("window.scrollBy(0, 10000);")
    time.sleep(5)



soup = BeautifulSoup(driver.page_source, 'html.parser')


print("Ingrese palabra a scrapear")
nombre = input()      

news_list = []

# Encontrar todos los headers en finance.yahoo
for h in soup.findAll('h3',class_='Mb(5px)'):
    news_title = h.findAll()[0].text

    if news_title not in news_list:
        if 'ad' not in news_title:
            news_list.append(news_title)


no_of_news = 0
keyword_list = []
    # Recorre la lista y busca la palabra clave
for i, title in enumerate(news_list):
    text = ''
    if nombre.lower() in title:
        text = ' <------------ Palabra clave'
        no_of_news += 1
        keyword_list.append(title)

    print(i + 1, ':', title, text)

    # Print de Titulos de los artulos que contienen los keywords
print(f'\n--------- Total menciones de "{nombre}" = {no_of_news} ---------')
for i, title in enumerate(keyword_list):
    print(i + 1, ':', title)

## Procesamiento Utilizando Librería Textblob

from textblob import TextBlob
keyword_list

news_sentblob = []
for news in keyword_list:
	print(news)
	analysis = TextBlob(news)
	print(analysis.sentiment)
	news_sentblob.append((news, analysis.sentiment[0], analysis.sentiment[1]))
    

news_sentblob

dfb = pd.DataFrame(news_sentblob, columns=['news','polaridad','subjetividad'])

dfb

# Exportar a csv

dfb.to_csv('base1.csv')

## Procesamiento Utilizando Librería Vadersentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
vs = analyzer.polarity_scores("This table is black")
print(vs)


for news in news_sentblob:
	print(news)
	analysis = analyzer.polarity_scores("news")
	print(analysis)
	news_sentblob.append((news, analysis))
    
## Se exporta lista news_sentblob a base2.csv

with open('base2.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=';')
    writer.writerows(news_sentblob)








































######################################
