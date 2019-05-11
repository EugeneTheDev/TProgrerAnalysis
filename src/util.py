import requests as req


def translate(text):
    response = req.get(url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t", params={
        "q": text
    }, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    })
    return response.json()[0][0][0]
