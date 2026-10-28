import requests
from bs4 import BeautifulSoup
import time
import csv
from collections import deque
from urllib.parse import urljoin, urlparse

start_url = "https://www.musashino-u.ac.jp"
res = requests.get(start_url)

visited = set()
queue = deque([start_url])
site_map = {}


html_soup = BeautifulSoup(res.content, "html.parser")

soup_title = html_soup.title

site_map = {}
site_map[start_url] = soup_title.string

print(site_map)

while queue:
    url = queue.popleft()

    if url in visited:
        continue

    visited.add(url)

    try:
        time.sleep(0.001)
        res = requests.get(url, timeout=10)

        soup = BeautifulSoup(res.content, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"

        site_map[url] = title

        for link in soup.find_all("a"):
            href = link.get("href")

            if not href:
                continue

            full_url = urljoin(url, href)

            if urlparse(full_url).netloc == "www.musashino-u.ac.jp":

                if full_url not in visited:
                    queue.append(full_url)

    except:
        pass

print(site_map)

with open("sitemap.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["URL", "Title"])

    for url, title in site_map.items():
        writer.writerow([url, title])