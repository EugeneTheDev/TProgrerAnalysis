import requests as req
from bs4 import BeautifulSoup


def translate(text):
    response = req.get(url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t", params={
        "q": text
    }, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    })
    return response.json()[0][0][0]


def get_text_from_image(url, language='rus'):
    payload = {'url': url,
               'apikey': "374e73777688957",
               "language": language
               }
    r = req.post('https://api.ocr.space/parse/image', data=payload)
    return r.json()["ParsedResults"][0]["ParsedText"]


def parse_hashtag_stats(hashtag):
    response = req.post(url="https://ritekit.com/api-demo/hashtag-stats", data={
        "hashtag": hashtag,
        "_do": "apiDemo-form-submit",
        "_submit": "Show hashtag stats"
    })
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("div", class_="alert alert-success") \
        .find_all("p")[6] \
        .get_text() \
        .replace("RiteKit recommendation (color)", "Score")
