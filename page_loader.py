import io
import re

import urllib3

from bs4 import BeautifulSoup


def extract_text(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

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


link = 'https://www.reddit.com/r/copypasta/'
soup = open_link(link)


with io.open('texts/reddit.txt', 'w', encoding='utf8') as f:
    for link in soup.findAll('a', attrs={'href': re.compile(link)}):
        f.write(extract_text(open_link(link.get('href'))))
# print(extract_text(soup))

