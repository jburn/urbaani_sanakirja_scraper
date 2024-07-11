import requests
import json
from constants import *
from bs4 import BeautifulSoup


def words_to_file(words):
    with open(OUT_FILE, "+w", encoding="utf-8") as wfile:
        json.dump(words, wfile, ensure_ascii=False)


with open("links.txt", "r") as rfile:
    links = [r.rstrip("\n") for r in rfile.readlines()]

length = len(links)
words = {}
for i, link in enumerate(links):
    r = requests.get(ROOT_URL + link)
    soup = BeautifulSoup(r.text, "html.parser")

    boxes = soup.find_all('div', {"class": "box"})
    try:
        header = boxes[0].find("h1")
    except:
        continue
    print(f"Scanning {(i/length)*100:.2f}% done. Scanning word {header.text}")
    words[header.text] = []
    for box in boxes:
        explanation = box.find("p")
        examples = box.find_all("blockquote")
        user = box.find("span", {"class": "user"})
        date = box.find("span", {"class": "datetime"})
        upvotes = box.find("button", {"class": "btn btn-vote-up rate-up"})
        downvotes = box.find("button", { "class": "btn btn-vote-down rate-down"})
        labels = box.find_all("span", {"class": ["label label-positive", "label label-negative"]})
        def_object = {
            "explanation": explanation.text,
            "examples": [quote.text.strip() for quote in examples],
            "user": user.text,
            "date": date.text,
            "upvotes": upvotes.text.strip(),
            "downvotes": downvotes.text.strip(),
            "labels": [label.text.strip() for label in labels]
        }
        words[header.text].append(def_object)
    if i % 100 == 0:
        words_to_file(words)
words_to_file(words)
