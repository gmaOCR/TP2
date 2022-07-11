import re
from urllib.request import ProxyDigestAuthHandler
import requests
import csv
from bs4 import BeautifulSoup
# Import hors projet à des fins de verif
import pandas as pd

#DECLARATION DES VARIABLES
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


#SOUP INDEX.HTML
index_url = "https://books.toscrape.com/"
category_link_list = []
page = requests.get(index_url)
if page.ok:
    soup = BeautifulSoup(page.text, 'html.parser')
    
# CREATION DES CSV INITIAUX
categorie = soup.select('a[href^="catalogue/category/books/"]')
for name in categorie:

    with open('.\CSV\librairie_' + name.text.strip() + '.csv' , 'w', encoding='UTF-8') as outfile:
        outfile.write('URL|UPC|Titre|Catégorie|Prix H.T.|Prix T.T.C|Description du produit|Stock|Note|URL de la couverture'+'\n')

# LIRE les URL de chaque categorie
a = soup.select('a[href^="catalogue/category/books/"]')
for href in a:
    link = href['href']
    category_link_list.append(index_url + link)
    
# POUR chaque URL de categorie lire les URL produits
product_URL_list = []
for select_URL in category_link_list:
    book_page = requests.get(select_URL)
    if book_page.ok:
        soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
        # print(soup_book_page)
    pagination = soup_book_page.select_one(".next")
    # print("avant if")
    URL_pagination = []
    if pagination is not None:
        # print("apres if")
        i = 0
        li_current = soup_book_page.find('li', class_='current')
        max_page = int(re.search("of (.*)", li_current.text).group(1))
        # TANT QUE pagination lire le lien "Next"
        while i < max_page:
            # print("aprés while")
            i = i + 1
            # print(i)
            URL_pagination.append(select_URL.replace("index.html","page-" + str(i) + ".html"))
            # print(URL_pagination)
        for select_URL in URL_pagination:
            book_page = requests.get(select_URL)
            print(select_URL)
            if book_page.ok:
                soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
        div = soup_book_page.findAll('div', class_="image_container")
        product_URL_list = []
        for a in div:
            href = a.select('a[href$="index.html"]')
            for href_url in href:
                link = href_url['href'].replace('../../..' , '')
                product_URL_list.append(index_url + 'catalogue' + link)
            # POUR chaque URL produit lire les données du produit                            
            for product_page_url in product_URL_list:
                # print(product_page_url)
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
            # ECRIRE les variables dans le fichier correspondant a la bonne categorie
                with open('librairie_' + category.text + '.csv','a', encoding='utf-8') as addfile:
                    addfile.write(product_page_url + '|' + universal_product_code + '|' + title.text + '|' + category.text + '|' +  price_excluding_tax + '|' + price_including_tax + '|' + product_description + '|' + number_available +  '|' + ratings + '|' + image_url + '\n')
    else: 
        div = soup_book_page.findAll('div', class_="image_container")
        for a in div:
            href = a.select('a[href$="index.html"]')
        for href_url in href:
            link = href_url['href'].replace('../../..' , '')
            # print(link)
            product_URL_list.append(index_url + 'catalogue' + link)
                
        # POUR chaque URL produit lire les données du produit
        for product_page_url in product_URL_list:
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
        # ECRIRE les variables dans le fichier correspondant a la bonne categorie
            with open('.\CSV\librairie_' + category.text + '.csv','a', encoding='utf-8') as addfile:
                addfile.write(product_page_url + '|' + universal_product_code + '|' + title.text + '|' + category.text + '|' +  price_excluding_tax + '|' + price_including_tax + '|' + product_description + '|' + number_available +  '|' + ratings + '|' + image_url + '\n')




# POUR chaque URL categorie lire les URL produits
# POUR chaque URL produit lire les variables
# Ecrire les variables dans le fichier correspondant a la bonne categorie
# REPETER le if jusqu'à sortir de la condition

        # for i in range(1,max_page + 1):
        #     if i == max_page:
       # i = 0
        #  i in range(1,max_page + 1):
        # li_current = soup_book_page.find('li', class_='current')
        # print(li_current.text)
        # max_page = int(re.search("of (.*)", li_current.text).group(1))
        # for href in pagination:
            # link = href['href']
            # URL_pagination.append(select_URL.replace("index.html","") + link.replace("page-2","page-" + str(i)))
        # print(select_URL)
        # else:
        #     for href in a:
        #         link = href['href'].replace('../../..' , '')
        #         product_URL_list.append(index_url + 'catalogue' + link)
        #         print(product_URL_list)

    #Boucle du nombre de page max de l'index
    # for i in range(1,max_page + 1):
    #     if i == max_page:
            # print(i)


