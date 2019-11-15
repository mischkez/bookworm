import re

import requests
from bs4 import BeautifulSoup


def price_format(price, for_display=False):
    price_list = re.findall(r"[+-]?\d+\,\d+|[+-]?\d+\.\d+", price.strip())
    first_element = price_list[0].replace(',', '.')

    if for_display:
        return first_element

    return float(first_element)


class SiteScrapper:

    def __init__(self, url, tag, clss, format='lxml'):
        print(url,tag,clss,format)
        self.url = url
        self.tag = tag
        self.clss = clss
        self.format = format
        
        request = requests.get(self.url)
        soup = BeautifulSoup(request.content, self.format)
        
        self.results = soup.find_all(self.tag, class_=self.clss)

    def scrap_the_data(self):
        raise NotImplementedError("Please Implement this method")        


class ThaliaScrapper(SiteScrapper):

    CLSS, TAG = 'product', 'div'

    def __init__(self, query):
        url = self.generate_url(query)
        super().__init__(url, self.TAG, self.CLSS)

    def generate_url(self, query):
        return f"https://www.thalia.at/suche?filterPATHROOT=c2&sq={query}&p=2&pagesize=40"

    def scrap_the_data(self):
        book_list = []

        for book in self.results:
            title = book.find('span', {'class': 'oProductTitle'}).text
            price = book.find('span', {'class': 'oPrice'}).text
            image = book.find('img').get('src')
            authors = book.find_all('span', class_='oAuthor')
            link = book.find('a', attrs={'data-info': 'product'}).get('href')

            author_list = []
            for author in authors:
                if author.text not in author_list:
                    author_list.append(author.text)

            book_dict = {
                'title': title,
                'price': price_format(price.strip()),
                'display_price': price_format(price.strip(), True),
                'image': image,
                'by': author_list,
                'link': 'https://www.thalia.at{}'.format(link)
            }

            book_list.append(book_dict)
        return book_list


class WeltbildScrapper(SiteScrapper):

    CLSS, TAG = 'listitem clearfix', 'article'

    def __init__(self, query):
        url = self.generate_url(query)
        super().__init__(url, self.TAG, self.CLSS)

    def generate_url(self, query):
        return f"https://www.weltbild.at/suche/{query}?anzahl=2&node=/buecher"

    def scrap_the_data(self):
        book_list = []

        for book in self.results:
            title = book.find('div', {'class': 'title'}).text
            price = book.find('div', {'class': 'price'}).text
            image = book.find('div', {'class': 'mediabox'}).find('img').get('data-src')
            authors = book.find_all('div', class_='author')
            link = book.find('a').get('href')

            author_list = []
            for author in authors:
                if author.text not in author_list:
                    author_list.append(author.text)

            book_dict = {
                'title': title,
                'price': price_format(price),
                'display_price': price_format(price, True),
                'image': image,
                'by': author_list,
                'link': 'https://www.weltbild.at{}'.format(link)
            }

            book_list.append(book_dict)
        return book_list
    
