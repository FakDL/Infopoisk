import zipfile
from bs4 import BeautifulSoup
import requests

counter = 0

def index_txt(link, i):
    f_index = open("index.txt", "a")
    pattern = "%d. %s\n"
    f_index.write(pattern % (i, link))
    f_index.close()


def make_archive(content):
    i = 0
    with zipfile.ZipFile('выкачка.zip', 'w') as f:
        for page in content:
            f.writestr("страница" + str(i) + ".html", page)
            i += 1


def find_links(html_page):
    links = []
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.findAll('a'):
        links.append(str(link.get('href')))

    return links


def open_url(url):
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
    except requests.exceptions.MissingSchema:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.InvalidURL:
        return None
    except requests.exceptions.InvalidSchema:
        return None
    if r.status_code == 200:
        global counter
        counter = counter + 1
        if counter != 0:
            index_txt(url, counter)
        return r.text
    else:
        return None


if __name__ == '__main__':
    host_url = 'https://ru.wikipedia.org'
    open("index.txt", "w").close()
    start_url = 'https://ru.wikipedia.org/wiki/Википедия:Избранные_статьи'
    start_page = open_url(start_url)
    links = find_links(start_page)
    links = links[:200]

    contents = []
    print('Открытие ссылок')
    for link in links:
        content = open_url(host_url + link)
        print(link)
        if content is not None:
            contents.append(content)
    print('Создание архива')
    make_archive(contents)
