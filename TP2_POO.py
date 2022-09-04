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



class CategoryLink(WebScrapping):
    def __init__(self):
        pass

    def get_link(self):
        category_link_list = []
        a = self.scrapper().select('a[href^="catalogue/category/books/"]')
        for href in a:
            link = href['href']
            category_link_list.append(index_url + link)
        print(category_link_list.append(index_url + link))
        return category_link_list.append(index_url + link)


class Books(CategoryLink):
    def __init__(self, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category, review_rating, image_url, name):
        super().__init__(name)
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


#instance classe mere
a = WebScrapping()
#methode classe mere
b = a.scrapper()
#instance classe fille
c = CategoryLink()
#methode classe fille
d = c.get_link()
#methode mere appliquée methode fille
e = c.scrapper()
print(d)


'''p = CategoryLink()

print(p.get_link())
#print(WebScrapping.scrapper(self=True))
'''
