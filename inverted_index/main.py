import zipfile
from tqdm import tqdm


def create_index():
    with zipfile.ZipFile("выкачка.zip") as myzip:

        with open("lemmas.txt", encoding="utf-8") as f:
            lines = f.readlines()
            lines = lines[:1000]

        inv_index = {}
        for line in tqdm(lines, desc="Processing lemmas"):
            term, lemmas = line.strip().split(": ")
            lemmas = lemmas.split()

            matches = set()

            for name in myzip.namelist():
                if name.endswith(".html"):
                    with myzip.open(name) as f:
                        html = f.read().decode("utf-8")
                    if any(lemma in html for lemma in lemmas):
                        matches.add(name)

            inv_index[term] = matches

    with open("inv_index.txt", "w") as f:
        for term, matches in tqdm(inv_index.items(), desc="Writing to file"):
            f.write(term + ": " + " ".join(matches) + "\n")


def boolean_search(query):
    inv_index = {}
    with open("inv_index.txt", "r") as f:
        for line in f:
            if ":" not in line:
                continue
            split = line.strip().split(": ")
            if len(split) == 1:
                continue
            matches = set(split[1].split())
            inv_index[split[0]] = matches

    if any(op in query for op in ["AND", "OR", "NOT"]):
        terms = query.split()
        params = ["OR"] * (len(terms) - 1)

        operators = []
        for i in range(len(terms)):
            if terms[i] in ["AND", "OR", "NOT"]:
                operators.append((i, terms[i]))

        terms = [term for term in terms if term not in ["AND", "OR", "NOT"]]

        for i, operator in operators:
            if operator == "AND":
                params[i - 1] = "AND"
            elif operator == "OR":
                params[i - 1] = "OR"
            elif operator == "NOT":
                params[i - 1] = "NOT"

        matches = None
        for i, term in enumerate(terms):
            if term in inv_index:
                if matches is None:
                    matches = inv_index[term].copy()
                else:
                    if params[i - 1] == "AND":
                        matches = matches.intersection(inv_index[term])
                    elif params[i - 1] == "OR":
                        matches = matches.union(inv_index[term])
                    elif params[i - 1] == "NOT":
                        matches = matches.difference(inv_index[term])
            else:
                if params[i - 1] == "AND":
                    matches = set()
                elif params[i - 1] == "OR":
                    continue
                elif params[i - 1] == "NOT":
                    matches = set(inv_index.keys()).difference(inv_index[term])

        if matches is None:
            print("Страниц не найдено.")
        else:
            for match in matches:
                print(match)
    else:
        if query in inv_index:
            for match in inv_index[query]:
                print(match)
        else:
            print("Страниц не найдено.")


if __name__ == '__main__':
    create_index()
    boolean_search("добывать AND ритуальный")
    # ВЫВОД:
    # страница116.html
    # страница118.html
    # страница193.html
