import re

import requests
from bs4 import BeautifulSoup


def price_format(price, for_display=False):
    price_list = re.findall(r"[+-]?\d+\,\d+|[+-]?\d+\.\d+", price.strip())
    first_element = price_list[0].replace(',', '.')

    if for_display:
        return first_element

    return float(first_element)


def tahlia_scrapper(q):
    """
    scraps the books from thalia.at 
    """
    url = 'https://www.thalia.at/suche?filterPATHROOT=c2&sq={}&p=2&pagesize=40'.format(
        q)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    books = soup.find_all('div', class_="product")

    book_list = []
    for book in books:
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


def weltbild_scrapper(q):
    """
    scraps the books from weltbild.at 
    """
    url = 'https://www.weltbild.at/suche/{}?anzahl=2&node=/buecher'.format(q)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    book_list = []
    books = soup.find_all('article', class_="listitem clearfix")

    for book in books:
        title = book.find('div', {'class': 'title'}).text
        price = book.find('div', {'class': 'price'}).text
        image = book.find('div', {'class': 'mediabox'}
                          ).find('img').get('data-src')
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
