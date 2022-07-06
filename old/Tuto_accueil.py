import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

rep = requests.get(url)

if rep.ok:
    soup = BeautifulSoup(rep.text, 'lxml')
   # liste = soup.findAll('li' )
    liste = soup.findAll(class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3' )
    #print(len(liste))
    [print(str(class_) + '\n\n') for class_ in liste]