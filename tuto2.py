import re
from unicodedata import category
import requests
import csv
from bs4 import BeautifulSoup

index_url = "https://books.toscrape.com/"
category_link_list = []
page = requests.get(index_url)
if page.ok:
    soup = BeautifulSoup(page.text, 'html.parser')
# Lire les URL de chaque categorie
a = soup.select('a[href^="catalogue/category/books/"]')
for href in a:
    link = href['href']
    category_link_list.append(index_url + link)
# print(category_link_list)

# POUR chaque URL categorie lire les URL produits (+ SI pagination) 
for select_URL in category_link_list:
    book_page = requests.get(select_URL)
    if book_page.ok:
        soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
        # print(soup_book_page)
        div = soup_book_page.find('div', class_="image_container")
        a = div.select('a[href$="index.html"]')
        for href in a:
            link = href['href']
            print(link)
        # a = soup_book_page.select('a[href$="index.html"]')
        # for href in a:
        #     link = href['href']
        #     print(link)
        

# POUR chaque produit extraire les données