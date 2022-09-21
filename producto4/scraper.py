import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import os
from datetime import date, timedelta
import re


#Consumimos una la funcion que hace todo el proceso para el día de ayer
exec(open("scraper_lib.py").read())
process_yesterday()
