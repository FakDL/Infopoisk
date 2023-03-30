import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Путь к папке с html страницами
pages_dir = "..\\tf_idf\\pages"

# Путь к папке с tf-idf леммами
tf_idf_lemmas_dir = "..\\tf_idf\\tf_idf_lemmas_page"

# Загрузка html страниц
pages = {}
for filename in os.listdir(pages_dir):
    with open(os.path.join(pages_dir, filename), "r", encoding="utf-8") as f:
        pages[filename] = f.read()


# Функция для загрузки словаря tf-idf лемм для каждой страницы
def load_tf_idf_lemmas(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        tf_idf = {}
        for line in lines:
            lemma, tf, idf = re.split(r"\s+", line.strip())
            tf_idf[lemma] = float(tf) * float(idf)
        return tf_idf


# Загрузка словарей tf-idf лемм для каждой страницы
tf_idf_lemmas = {}
for filename in os.listdir(tf_idf_lemmas_dir):
    tf_idf_lemmas[filename] = load_tf_idf_lemmas(os.path.join(tf_idf_lemmas_dir, filename))

# Создание векторизатора tf-idf
vectorizer = TfidfVectorizer()

# Обучение векторизатора на леммах всех страниц
lemmas_corpus = [" ".join(tf_idf_lemmas[filename].keys()) for filename in tf_idf_lemmas.keys()]
vectorizer.fit_transform(lemmas_corpus)


# Функция для преобразования запроса в вектор tf-idf
def query_to_vector(query):
    query_vector = vectorizer.transform([query])
    return query_vector.toarray()[0]


# Функция для вычисления косинусного расстояния между двумя векторами
def cosine_distance(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# Функция для поиска страниц на основе запроса
def search(query, tf_idf_dict):
    query_vector = query_to_vector(query)
    results = []
    for filename, tf_idf in tf_idf_dict.items():
        page_vector = [tf_idf.get(word, 0) for word in vectorizer.get_feature_names_out()]
        similarity = cosine_distance(query_vector, page_vector)
        results.append((filename, similarity))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# Пример использования функции search
query = "первомайский"
results = search(query, tf_idf_lemmas)
for filename, similarity in results[:10]:
    print(f"page_{filename.split('_')[-1].split('.')[0]}: {similarity}")
