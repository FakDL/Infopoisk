import re
import string
import zipfile
import nltk
import pymorphy2
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()

def set_token(result):
    index_html = open("tokens.txt", "a")
    pattern = "%s\n"

    # формат: <токен><\n>
    for word in result:
        index_html.write(pattern % word)
    index_html.close()

def read_file(zip_file, f):
    html = zip_file.open(f)
    return html

def punctuation_marks_filtering(values):
    return [i for i in values if all(not j in string.punctuation for j in i)]

def garbage_filtering(word):
    # фильтрация мусора
    rus = re.compile(r'^[а-яА-Я]{2,}$')
    numbers = re.compile(r'^[0-9]+$')

    res = bool(rus.match(word)) or bool(numbers.match(word))
    return res


def get_tokens(html):
    page_content = BeautifulSoup(html).get_text()

    result = list(nltk.wordpunct_tokenize(page_content))
    result = punctuation_marks_filtering(result)
    result = list(filter(garbage_filtering, result))

    return result

def get_lemma(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


def set_lemmas(lemma_resource):
    f_lemma = open("lemmas.txt", "a")

    # формат: <лемма><пробел><токен 1><пробел><токен 2>.....<пробел><токенN><\n>
    for lemma, tokens in lemma_resource.items():
        f_words = lemma + ": "
        for token in tokens:
            f_words += token + " "
        f_words += "\n"
        f_lemma.write(f_words)
    f_lemma.close()


def lemma(token_resource):
    lemma_arr = dict()
    for word in token_resource:
        normal_form = get_lemma(word)
        if not normal_form in lemma_arr:
            lemma_arr[normal_form] = []
        lemma_arr[normal_form].append(word)
    return lemma_arr


if __name__ == '__main__':
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('snowball_data')
    nltk.download('perluniprops')
    nltk.download('universal_tagset')
    nltk.download('stopwords')
    nltk.download('nonbreaking_prefixes')
    nltk.download('wordnet')

    fileZip = zipfile.ZipFile('выкачка.zip', 'r')
    token_resource = set()

    for f in fileZip.filelist:
        page_html = read_file(fileZip, f.filename)
        token_file = set(get_tokens(page_html))
        token_resource = token_resource | token_file

    set_token(token_resource)
    lemma_resource = lemma(token_resource)
    set_lemmas(lemma_resource)