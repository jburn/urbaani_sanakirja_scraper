import requests
from constants import *
from bs4 import BeautifulSoup


def write_to_file(links):
    with open(LINK_FILE, "a+") as wfile:
        wfile.writelines(links)

# get links to all words
for t in range(len(BROWSE_TABS)):
    print(BROWSE_ROOT_URL + BROWSE_TABS[t])
    r = requests.get(BROWSE_ROOT_URL + BROWSE_TABS[t])
    if r.status_code != 200:
        print(f"ERROR: HTML {r.status_code}")
        exit(1)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all('a')
    page_links = [int(l.get("href").split("=")[-1]) for l in links if l.get("href").startswith("?page=")]
    pages = 1
    if len(page_links) > 0:
        pages = max(page_links)
    print(f"Pages: {pages}")
    for page in range(1, pages+1):
        print(f"\t{BROWSE_ROOT_URL + BROWSE_TABS[t]}/?page={page}")
        pr = requests.get(BROWSE_ROOT_URL + BROWSE_TABS[t] + f"/?page={page}")
        if pr.status_code != 200:
            print(f"ERROR: HTML {pr.status_code}")
            exit(1)
        psoup = BeautifulSoup(pr.text, "html.parser")
        wordl = psoup.find_all('a')
        words_to_add = [l.get("href") + "\n" for l in wordl if l.get("href").startswith("/word/")]
        write_to_file(words_to_add)
