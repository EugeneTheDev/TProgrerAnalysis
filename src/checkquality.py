import requests as req


def check_orthography(text):
    response = req.post(url="https://speller.yandex.net/services/spellservice.json/checkText?options=12", data={
        "text": text
    }).json()

    print(response)

    if response:
        for el in response:
            text = text[:el["pos"]] + text[el["pos"]:el["pos"] + el["len"]].replace(el["word"], el["s"][0])\
                   + text[el["pos"] + el["len"]:]

    print(text)


def check_image(url, width, height):
    if 680 < width < 720 and 480 < height < 520:
        return True
    else:
        return False


def check_link(url):
    response = req.get(url=url)
    if response.ok:
        return True
    else:
        return False

def ocr_space_url(url, overlay=False, api_key='374e73777688957', language='rus'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': "374e73777688957",
               'language': language,
               }
    r = req.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

print(ocr_space_url("https://sun1-24.userapi.com/c635106/v635106619/2ab15/1JGyBVzkfcY.jpg"))
