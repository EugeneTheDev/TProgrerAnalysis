import re

import requests as req
from bs4 import BeautifulStoneSoup


def read_news():
    feed = req.get("https://www.google.com/alerts/feeds/03091274654750541825/1956891941018950863")
    soup = BeautifulStoneSoup(feed.text)

    response = []
    for el in soup.find_all("entry")[-30:]:
        title = el.find("title").get_text().replace("&#39;", "`").replace("&nbsp;", " ").replace("&quot;", "'")
        link = el.find("link")["href"]
        content = el.find("content").get_text().replace("&#39;", "`").replace("&nbsp;", " ").replace("&quot;", "'")

        if "Google Alert - " not in title:
            url = re.findall(r"url=.+&ct", link)[0].replace("url=", "").replace("&ct", "").replace("%3F", "?")\
                .replace("%3D", "=").replace("%26", "&")
            response.append({
                "title": title,
                "content": content,
                "link": url
            })

    return response


for el in read_news():
    print(el["title"], el["content"], el["link"], "\n", sep="\n")
