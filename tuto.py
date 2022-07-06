# import string
# import sys
from ast import Continue
import re
import requests
import csv
from bs4 import BeautifulSoup

#Objectifs
product_page_url = []
universal_product_code = []
tiltle = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

#Création du CSV de la libraire en ligne
with open('librairie_totale.csv', 'w', encoding="utf-8") as outfile:
    outfile.write('URL|UPC|Titre|Catégorie|Prix H.T.|Prix T.T.C.|Description du produit|Stock|Note|URL de la couverture'+'\n')

# URL et soup
index_url = "https://books.toscrape.com"
books_links_index = []
category_list = []
rep = requests.get(index_url)
if rep.ok:
    soup = BeautifulSoup(rep.text, 'html.parser')
#Extrais le nombre de page d'index max
li_current = soup.find('li', class_='current')
max_page = int(re.search('of (.+.)', li_current.text).group(1))
#Extrais le lien en STR de l'index général de toute la librairie en ligne
nav_list = soup.find( 'ul', class_='nav nav-list')
a = nav_list.find('a')
index_link = a['href']
books_links_index.append('https://books.toscrape.com/' + index_link)
#uniformise la syntaxe du lien en vue l'incrément
books_link = books_links_index[0].replace("index.html","",)
links = []
p_links = []
i = 0
#Defini le nombre de pages index max
for i in range(1,max_page + 1):
    if i == max_page:
        break
    # Incremente le lien d'index de 20 libres (page-n puis n+1)
    books_index_list = books_link + 'page-' + str(i) + '.html'
    links.append(books_index_list)
    page = requests.get(books_index_list)
    if page.ok:
            soup_index = BeautifulSoup(page.text, 'html.parser')
            image_container = soup_index.findAll( 'div', class_='image_container')
# Dresse la liste de tous les liens des produits
            for product in image_container:
                a = product.find('a')
                p_link = a['href'].split('../..')
                p_links.append(books_link.replace("/category/books_1/","") + p_link[1])
# Boucle a liste de liens pour lire chaque page produit
for product_page_url in p_links:
# Soup des données par page produit
    rep2 = requests.get(product_page_url)
    if rep2.ok:
        soup = BeautifulSoup(rep2.text, 'html.parser')
    #Extrais les <td> en liste  
    liste_td = soup.findAll('td')
#Extrais la liste sur les variables finales
    row = [i.text for i in liste_td]
    universal_product_code = row[0]
    price_excluding_tax = row[2].replace("Â","",)
    price_including_tax = row[3].replace("Â","",)
    number_available = row[5] 
#Extrais le href contenant la catégorie
    breadcrumb = soup.find( 'ul', class_='breadcrumb') 
    cat = breadcrumb.select('a[href^="../category/books/"]')
    for category in cat:
        category.findNext(text="index.html")
#Extrais le titre
    title = soup.find('h1')
#Extrais le product description
    product_description = soup.find( 'p', attrs={'class': None})
    if product_description is not None:
        product_description = product_description.text
    else:
        product_description = "Vide"
        print(product_description)
#Extrais et test la valeur de la note
    div = soup.find('div', class_='col-sm-6 product_main')
    ratings = div.select_one('p.star-rating').get('class')[-1]
    if ratings == "One":
        review_rating = 1
    elif ratings == "Two":
        review_rating = 2
    elif ratings == "Three":
        review_rating = 3
    elif ratings == "Four":
        review_rating = 4
    elif ratings == "Five":
        review_rating = 5
    else:
        review_rating = "N/A"                    
    #Extrais l'URL de l'image du produit        
    item_active = soup.find( 'div', class_='item active')
    img = item_active.find('img')
    link_split = img['src'].split('../..')
    image_url ='https://books.toscrape.com' + link_split[1]
    
    #Ecriture des résultats
    with open('librairie_totale.csv','a', encoding="utf-8") as addfile:
        addfile.write(product_page_url + '|' + universal_product_code + '|' + title.text + '|' + category.text + '|' +  price_excluding_tax + '|' + price_including_tax + '|' + product_description + '|' + number_available +  '|' + review_rating + '|' + image_url + '\n') 
