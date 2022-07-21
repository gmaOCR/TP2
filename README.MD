# Webscrapping

Ce script permet d'extraire les données des livres du site https://books.toscrape.com/ 
à des fins de formation

## Installation et lancement - Exécutez les commandes suivantes

```bash
$ git clone https://github.com/marianigregory/OpenClass.git
$ cd OpenClass
$ mkdir IMG
$ mkdir CSV
$ python -m venv env
$ env/bin/pip install -r requirements.txt
$ env/bin/python TP2.py

Les résultats données sont classés par catégorie de livre dans le répertoire CSV: un fichier par catégorie.
Les résultats images sont classés dans IMG par titre de livre précédés d'un numero unique.

Le délimiteur est un pipe: |

product_page_url 
universal_product_code 
tiltle 
price_including_tax 
price_excluding_tax 
number_available 
product_description 
category 
review_rating 
image_url URL 
