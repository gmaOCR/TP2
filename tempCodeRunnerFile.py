            for URL in URL_pagination:
                book_page = requests.get(URL)
                print(URL)