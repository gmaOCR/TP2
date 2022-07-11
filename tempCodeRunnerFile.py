               for href_url in href:
                        link = href_url['href'].replace('../../..' , '')
                        product_URL_list.append(index_url + 'catalogue' + link)
                        print("Valeur de PUL", product_URL_list)