#!env python
import requests
from bs4 import BeautifulSoup
import sys

def search_arxiv(subject):
    url = f"https://arxiv.org/search/?query={subject}&searchtype=all&source=header"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = [t.text for t in soup.find_all('p', {'class': 'title'})]
    abstracts = [a.text for a in soup.find_all('span', {'class': 'abstract-full has-text-grey-dark mathjax'})]
    for i in range(len(titles)):
        print(f"Title: {titles[i].strip()}")
        print(f"Abstract: {abstracts[i][9:-16]}\n")

search_arxiv(sys.argv[1])

