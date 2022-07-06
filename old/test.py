import requests
from bs4 import BeautifulSoup

#Objectifs
url = "https://books.toscrape.com/"
links =[]
category_list = []
cat = "Classics"
page = requests.get(url)
if page.ok:
        soup = BeautifulSoup(page.text, 'html.parser')
for a in soup.select('a[href^="catalogue/category"]'):
    for b in a.children:
        category_list.append(b.strip(' \n'))
# print(category_list)

# ul = soup.find('ul', class_='nav nav-list')
# print(ul)
# a = ul.find_all('a')
# data = []
# for link in a:
#     data.append(link.text)
# print(data)



    # print(category_list)

# for i in range(0, len(category_list)):
#     print(category_list)
# for cat in category_list:
#  with open('librairie_' + str(cat) +'totale.csv', 'w', encoding="utf-8") as outfile:
#        outfile.write('Test'+'\n')