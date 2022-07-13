import re
from urllib.request import ProxyDigestAuthHandler
import requests
import csv
from bs4 import BeautifulSoup

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

# CARACTERES INTERDITS SUR NOMMAGE DES FICHIERS
to_replace = {'/' : ' ', '\\' : ' ', ',': ' ', '#': ' ', ':': ' ', "\"": "'", "*": "_", "?": " "}

#SOUP INDEX.HTML
index_url = "https://books.toscrape.com/"
category_link_list = []
page = requests.get(index_url)
if page.ok:
    soup = BeautifulSoup(page.text, 'html.parser')
    
# CREATION DES CSV INITIAUX
categorie = soup.select('a[href^="catalogue/category/books/"]')
for name in categorie:
    with open('CSV/librairie_' + name.text.strip() + '.csv' , 'w', encoding='UTF-8') as outfile:
        outfile.write('URL|UPC|Titre|Catégorie|Prix H.T.|Prix T.T.C|Description du produit|Stock|Note|URL de la couverture'+'\n')

# LIRE les URL de chaque categorie
a = soup.select('a[href^="catalogue/category/books/"]')
for href in a:
    link = href['href']
    category_link_list.append(index_url + link)
# print(category_link_list)
    
# POUR chaque URL de categorie lire les URL produits
product_URL_list = []
for select_URL in category_link_list:
    book_page = requests.get(select_URL)
    if book_page.ok:
        soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
        # print(soup_book_page)
    pagination = soup_book_page.select_one(".current")
    # print(pagination)
    # print("avant if")
    
    if pagination is not None:
        # print("apres if")
        li_current = soup_book_page.find('li', class_='current')
        max_page = int(re.search("of (.*)", li_current.text).group(1))
        # TANT QUE pagination lire le lien "Next"
        i = 1
        URL_pagination = []
        while i <= max_page:
            URL_pagination.append(select_URL.replace("index.html","page-" + str(i) + ".html"))
            i = i + 1
        # print("Valeur URL PAG", URL_pagination)
        # k = 0
        # print("Valeur de K avant FOR", k)
        product_URL_list = []
        for URL in URL_pagination:
            # k = k+1
            # print("Valeur de K dans FOR", k)
            # print("Valeur de URL", URL)
            book_page = requests.get(URL)
            if book_page.ok:
            # print(book_page)
                soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
            div = soup_book_page.findAll('div', class_="image_container")
            for a in div:
                href = a.select('a[href$="index.html"]')
                for href_url in href:
                    link = href_url['href'].replace('../../..' , '')
                    product_URL_list.append(index_url + 'catalogue' + link)
            # print("Nombre de produit cumulé", len(product_URL_list))
        # POUR chaque URL produit lire les données du produit                            
        i = 0
        for product_page_url in product_URL_list:
            i = i + 1
            # print( "Product_page_url:    ", str(i),"       ", product_page_url)
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
            # print("i avant écriture:    ", i)
            title = title.text.translate(str.maketrans(to_replace))
            with open('CSV/librairie_' + category.text + '.csv','a', encoding='utf-8') as addfile:
             addfile.write(product_page_url + ' | ' + universal_product_code + ' | ' + title + ' | ' + category.text + ' | ' +  price_excluding_tax + ' | ' + price_including_tax + ' | ' + product_description + ' | ' + number_available +  ' | ' + ratings + ' | ' + image_url + '\n')
            img = requests.get(image_url)
            with open('IMG/' + (title) + ".jpg",'wb') as f:
                f.write(img.content)
    else: 
        # j = 0
        product_URL_list = []
        pagination = soup_book_page.select_one(".current")
        # print("j avant écriture:    ", j)
        if pagination is None:
            # print(pagination)
            div = soup_book_page.findAll('div', class_="image_container")
            for a in div:
                href = a.select('a[href$="index.html"]')
                for href_url in href:
                    link = href_url['href'].replace('../../..' , '')
                    # print(link)
                    product_URL_list.append(index_url + 'catalogue' + link)       
            # POUR chaque URL produit lire les données du produit
            for product_page_url in product_URL_list:
                # j = j + 1
                # print( "Product_page_url:    ", str(j),"       ", product_page_url)
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
                title = title.text.translate(str.maketrans(to_replace))
                with open('CSV/librairie_' + category.text + '.csv','a', encoding='utf-8') as addfile:
                    addfile.write(product_page_url + ' | ' + universal_product_code + ' | ' + title + ' | ' + category.text + ' | ' +  price_excluding_tax + ' | ' + price_including_tax + ' | ' + product_description + ' | ' + number_available +  ' | ' + ratings + ' | ' + image_url + '\n')
                img = requests.get(image_url)
                with open('IMG/' + (title)  + ".jpg",'wb') as f:
                    f.write(img.content)