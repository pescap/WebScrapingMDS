import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

W='\033[0m'
R='\033[31m'
G='\033[32m'

my_color= [W,R,G]

URL=requests.get("https://www.biobiochile.cl")
soup=BeautifulSoup(URL.text,'html.parser')

# COMENTAR GRANTITULAR Y DESCOMENTAR EL SEGUNDO SI QUIERES VER TODOS LOS TITULARES
#grantitular= soup.find("div", {"class": "gran-titular-aside-container"})
#headlines=grantitular.select("h2.article-title")

#DESCOMENTAR 
headlines=soup.select("h2.article-title")
largo=(len(headlines))

def get_element_txt(list_of_elements,n):
    number_elements=n
    elements=list_of_elements
    element_text= []
    for i in range(number_elements):
        element_text.append(elements[i].get_text())
    return element_text

def print_list_articles(source,list):
    data = list
    for element in data:
        print(random.choice(my_color)+'['+source+']['+str(datetime.now().time())+']'+element.upper())

print_list_articles('BIOBIOCHILE',get_element_txt(headlines,largo))
