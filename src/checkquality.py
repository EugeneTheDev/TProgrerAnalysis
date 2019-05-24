import re

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
        result += "Image too small\n"

    if width/height < 0.8 or width/height > 2:
        result += "Bad proportions\n"

    if util.get_text_square_from_image(url) > 0.2:
        result += "Too many text on image"

    return result


def check_link(url):
    try:
        response = req.get(url=url, timeout=5)
    except ConnectionError:
        return "Link doesnt work"

    if response.ok:
        return ""
    else:
        return "Link doesnt work"


def check_tags(text):
    tags = [el.replace("#", "") for el in re.findall(r"#[а-яА-Я@\w]+", text)]
    if not tags:
        tags_suggestions = util.parse_hashtag_suggestion(text)
        return f"{'Suggestion: '.join(tags_suggestions) if len(tags_suggestions) > 0 else ''}"
    elif len(tags) > 4:
        return "Too many tags (best between 2 and 4)"

    return ""


def perform_full_analysis(post):
    report = {}

    if "text" in post:
        orth_response = check_orthography(post["text"])
        report["text"] = {
            "send": orth_response == "",
            "message": orth_response
        }

        tags_response = check_tags(post["text"])
        report["tags"] = {
            "send": tags_response == "",
            "message": tags_response
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

