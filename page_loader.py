import io
import re

import urllib3

from bs4 import BeautifulSoup


def extract_text(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    div = soup.find("div", {"id": "mw-content-text"})
    try:
        for tag in soup.find_all(['h4', 'h3', 'h2', 'h1', 'a', 'link']):
            tag.decompose()
        for tag in soup.find_all('table', {'id': 'toc'}):
            tag.decompose()
    except:
        pass

    # get text
    text = div.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    return '\n'.join(chunk for chunk in chunks if chunk)


def open_link(link):
    print(link)
    http = urllib3.PoolManager()
    r = http.request('GET', link)
    page = r.data
    return BeautifulSoup(page)


# link = 'http://lurkmore.to/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2'
# link = 'http://lurkmore.to/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2&printable=yes&pagefrom=%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F+%D0%BB%D1%8E%D0%B1%D0%BE%D0%B2%D1%8C%0A%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F+%D0%BB%D1%8E%D0%B1%D0%BE%D0%B2%D1%8C#mw-pages'
# link = 'http://lurkmore.to/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2:Creepy'
# link = 'http://lurkmore.to/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2:%D0%90%D0%B2%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B0%D1%8F'
# link = 'http://lurkmore.to/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2:%D0%AD%D0%BF%D0%B8%D1%87%D0%BD%D0%B0%D1%8F'
link = 'http://lurkmore.to/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%90%D1%80%D1%85%D0%B8%D0%B2:%D0%A2%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F'


soup = open_link(link)

with io.open('texts/pasta_chan.txt', 'a', encoding='utf8') as f:
    for page in soup.findAll('a'):
        href = page.get('href')
        if isinstance(href, str):
            if href.startswith('/%D0%9A%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0'):
                f.write(extract_text(open_link("http://lurkmore.to" + page.get('href'))))
# print(extract_text(soup))
