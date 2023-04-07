import tkinter as tk
from tkinter import messagebox
from search.search import search
import zipfile
import tempfile
import webbrowser

pages_dir = "../inverted_index/выкачка.zip"


def extract_page(page_number):
    filename = f"страница{page_number}.html"
    with zipfile.ZipFile(pages_dir) as myzip:
        with myzip.open(filename) as myfile:
            return myfile.read().decode('utf-8')


def search_and_display():
    query = search_bar.get()
    results = search(query)
    if not results:
        messagebox.showinfo("Search Results", "ничего не найдено.")
        return

    results_listbox.delete(0, tk.END)
    for result in results:
        if result[1] > 0:
            page_number = result[0]
            page_filename = f"страница{page_number}.html"
            results_listbox.insert(tk.END, page_filename)


def open_selected():
    selected_index = results_listbox.curselection()
    if not selected_index:
        return

    selected_item = results_listbox.get(selected_index)
    page_number = selected_item[8:-5]
    html = extract_page(page_number)

    temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding='utf-8')
    temp_file.write(html)
    temp_file.close()

    webbrowser.open(f"file://{temp_file.name}")


root = tk.Tk()
root.title("Поиск")

search_bar = tk.Entry(root, width=50)
search_bar.pack()

search_button = tk.Button(root, text="Search", command=search_and_display)
search_button.pack()

results_listbox = tk.Listbox(root, height=30, width=50)
results_listbox.pack()

open_button = tk.Button(root, text="Открыть", command=open_selected)
open_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
