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

