import requests
import re
from bs4 import BeautifulSoup
import textwrap

#reference
index_url = "https://books.toscrape.com/"

class WebScrapping:
    def __init__(self):
        pass


    def scrapper(self):
        page = requests.get(index_url)
        if page.ok:
            soup = BeautifulSoup(page.text, 'html.parser')
            return soup

class CreateCSV(WebScrapping):
    def __init__(self):
        pass

    def create(self):
        s = self.scrapper()
        categorie = s.select('a[href^="catalogue/category/books/"]')
        for name in categorie:
            with open('CSV2/librairie_' + name.text.strip() + '.csv' , 'w', encoding='UTF-8') as outfile:
                outfile.write('URL|UPC|Titre|Catégorie|Prix H.T.|Prix T.T.C|Description du produit|Stock|Note|URL de la couverture'+'\n')

class CategoryLink(WebScrapping):
    def __init__(self):
        pass

    def get_link(self):
        s = self.scrapper()
        category_link_list = []
        a = s.select('a[href^="catalogue/category/books/"]')
        for href in a:
            link = href['href']
            category_link_list.append(index_url + link)
        return category_link_list

class ProductLink(CategoryLink):
    def __init__(self):
        pass

    def get_book_link(self):
        s = self.get_link()
        product_URL_list = []
        i = 0
        max_page = 0
        for select_URL in s:
            book_page = requests.get(select_URL)
            if book_page.ok:
                soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
            pagination = soup_book_page.select_one(".current")
            # CONDITION SI PAGINATION
            if pagination is not None:
                li_current = soup_book_page.find('li', class_='current')
                max_page = int(re.search("of (.*)", li_current.text).group(1))
                URL_pagination = []
                i = 1
                while i <= max_page:
                    URL_pagination.append(select_URL.replace("index.html","page-" + str(i) + ".html"))
                    i = i + 1
                    #CREER LA LISTE DES URL PRODUITS
                for URL in URL_pagination:
                    book_page = requests.get(URL)
                    if book_page.ok:
                        soup_book_page = BeautifulSoup(book_page.text, 'html.parser')
                    div = soup_book_page.findAll('div', class_="image_container")
                    for a in div:
                        href = a.select('a[href$="index.html"]')
                        for href_url in href:
                            link = href_url['href'].replace('../../..' , '')
                            product_URL_list.append(index_url + 'catalogue' + link)
                  #  print("if " + str(len(product_URL_list)))
            else:
               #product_URL_list = []
                pagination = soup_book_page.select_one(".current")
                # VERIFICATION ABSENCE PAGINATION
                if pagination is None:
                    div = soup_book_page.findAll('div', class_="image_container")
                    for a in div:
                        href = a.select('a[href$="index.html"]')
                        for href_url in href:
                            link = href_url['href'].replace('../../..' , '')
                            product_URL_list.append(index_url + 'catalogue' + link)
                   # print("else " + str(len(product_URL_list)))
        #print("FINAL " + str(len(product_URL_list)))
        return product_URL_list

class Books(ProductLink):
    def __init__(self):
        pass
        '''    
        self.product_page_url = product_page_url
        self.universal_product_code = universal_product_code
        self.title = title
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url
        '''
    def get_data(self):
        s = self.get_book_link()
        j = 0
        for product_page_url in s:
            j = j + 1
            print(j)
            rep2 = requests.get(product_page_url)
            if rep2.ok:
                soup = BeautifulSoup(rep2.text, 'html.parser')
            # Extrais les <td> en liste
            liste_td = soup.findAll('td')
            # Extrais la liste sur les variables finales
            row = [i.text for i in liste_td]
            self.universal_product_code = row[0]
            self.price_excluding_tax = row[2].replace("Â", "", )
            self.price_including_tax = row[3].replace("Â", "", )
            self.number_available = row[5]
            # Extrais le href contenant la catégorie
            breadcrumb = soup.find('ul', class_='breadcrumb')
            cat = breadcrumb.select('a[href^="../category/books/"]')
            for category in cat:
                category.findNext(text="index.html")
            # Extrais le titre
            self.title = soup.find('h1')
            # Extrais le product description
            product_description = soup.find('p', attrs={'class': None})
            if product_description is not None:
                self.product_description = product_description.text
            else:
                product_description = "Vide"
            # Extrais et test la valeur de la note
            div = soup.find('div', class_='col-sm-6 product_main')
            ratings = div.select_one('p.star-rating').get('class')[-1]
            if ratings == "One":
                self.review_rating = 1
            elif ratings == "Two":
                self.review_rating = 2
            elif ratings == "Three":
                self.review_rating = 3
            elif ratings == "Four":
                self.review_rating = 4
            elif ratings == "Five":
                self.review_rating = 5
            else:
                self.review_rating = "N/A"
            # Extrais l'URL de l'image du produit
            item_active = soup.find('div', class_='item active')
            img = item_active.find('img')
            link_split = img['src'].split('../..')
            self.image_url = 'https://books.toscrape.com' + link_split[1]
            # ECRIRE les variables dans le fichier correspondant a la bonne categorie
            self.title = title.text.translate(str.maketrans(to_replace))
            self.title = textwrap.shorten(title, width=50)
            self.title = re.sub(r"[^a-zA-Z0-9]+", ' ', title)
            book_num = product_page_url[-14:-11]
            """
            with open('CSV/librairie_' + category.text + '.csv', 'a', encoding='utf-8') as addfile:
                addfile.write(
                    product_page_url + ' | ' + universal_product_code + ' | ' + title + ' | ' + category.text + ' | ' + price_excluding_tax + ' | ' + price_including_tax + ' | ' + product_description + ' | ' + number_available + ' | ' + ratings + ' | ' + image_url + '\n')
            img = requests.get(image_url)
            with open('IMG/' + book_num + "_" + title + ".jpg", 'wb') as f:
                f.write(img.content) 
      """


#instance classe mere
a = WebScrapping()
#methode classe mere
b = a.scrapper()
#instance classe fille
c = CategoryLink()
#methode classe fille
d = c.get_link()
#methode mere appliquée classe fille
e = c.scrapper()


#Get book link
#f = ProductLink()
#g = f.get_book_link()
#print(g)

h = Books()
print (h.get_data())


'''p = CategoryLink()

print(p.get_link())
#print(WebScrapping.scrapper(self=True))

, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category, review_rating, image_url
'''
