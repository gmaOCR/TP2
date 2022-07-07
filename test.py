import re
import requests
import csv
from bs4 import BeautifulSoup

index_url = "https://books.toscrape.com/"
category_list = []
rep = requests.get(index_url)
if rep.ok:
    soup = BeautifulSoup(rep.text, 'html.parser')

    
    
    
    
    
    
    
    
    # for a in soup.select('a[href^="catalogue/category"]'):
    #     for b in a.children:
    #         category_list.append(b.strip(' \n'))
    #         print(category_list)