import requests
import re
from bs4 import BeautifulSoup
import textwrap


class Site:
    def __init__(self, url):
        self.url = url

    def soup(self):
        page = requests.get(self.url)
        if page.ok:
            soup = BeautifulSoup(page.text, 'html.parser')
            return soup

    def createCSV(self):
        s = self.soup()
        categorie = s.select('a[href^="catalogue/category/books/"]')
        for name in categorie:
            with open('CSV2/librairie_' + name.text.strip() + '.csv', 'w', encoding='UTF-8') as outfile:
                outfile.write(
                    'URL|UPC|Titre|Catégorie|Prix H.T.|Prix T.T.C|Description du produit|Stock|Note|URL de la couverture' + '\n')

    def get_cat_link(self):
        s = self.soup()
        category_link_list = []
        a = s.select('a[href^="catalogue/category/books/"]')
        for href in a:
            link = href['href']
            category_link_list.append(self.url + link)
        return category_link_list


class Category:

    def get_link(self):
        s = self.scrapper()
        category_link_list = []
        a = s.select('a[href^="catalogue/category/books/"]')
        for href in a:
            link = href['href']
            category_link_list.append(index_url + link)
        return category_link_list

a = Site(url="https://books.toscrape.com/")
a.createCSV()
liste_categorie = a.get_cat_link()

