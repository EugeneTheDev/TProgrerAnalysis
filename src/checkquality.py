import requests as req
from requests.exceptions import ConnectionError

from src import util


def check_orthography(text):
    response = req.post(url="https://speller.yandex.net/services/spellservice.json/checkText?options=12", data={
        "text": text
    }).json()

    if response:
        for el in response:
            text = text[:el["pos"]] + text[el["pos"]:el["pos"] + el["len"]].replace(el["word"], el["s"][0])\
                   + text[el["pos"] + el["len"]:]
        return text
    else:
        return ""


def check_image(url, width, height):
    result = ""
    if width < 700 and height < 500:
        result += "Изображение слишком маленькое (должно быть больше 700х500)\n"

    if width/height < 0.8 or width/height > 2:
        result += "Плохие пропорции\n"

    if util.get_text_square_from_image(url) > 0.2:
        result += "Слишком много текста на изображении\n"

    return result


def check_link(url):
    message = "Ссылка не работает или слишком долго загружается"
    try:
        response = req.get(url=url, timeout=5)
    except ConnectionError:
        return message

    if response.ok:
        return ""
    else:
        return message


def perform_full_analysis(post):
    report = {}

    if "text" in post:
        orth_response = check_orthography(post["text"])
        report["text"] = {
            "send": orth_response == "",
            "message": orth_response
        }

    if "images" in post:
        report["images"] = []
        for image in post["images"]:
            image_response = check_image(image["url"], image["width"], image["height"])
            report["images"].append({
                "send": image_response == "",
                "message": image_response
            })

    if "url" in post:
        link_response = check_link(post["url"])
        report["link"] = {
            "send": link_response == "",
            "message": link_response
        }

    return report

