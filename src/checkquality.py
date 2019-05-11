import re

import requests as req
from requests.exceptions import ConnectionError

from src import util


def check_orthography(text):
    response = req.post(url="https://speller.yandex.net/services/spellservice.json/checkText?options=12", data={
        "text": text
    }).json()

    if response:
        err_count = 0
        for el in response:
            text = text[:el["pos"]] + text[el["pos"]:el["pos"] + el["len"]].replace(el["word"], el["s"][0])\
                   + text[el["pos"] + el["len"]:]
            err_count += 1
        return text, err_count
    else:
        return "OK", 0


def check_image(url, width, height):
    text = util.get_text_from_image(url)
    if not 80 < len(text) < 130:
        if 680 < width < 720 and 480 < height < 520:
            return "OK", 0
        else:
            return "Bad image size (700x500 is the best)", 1
    else:
        return "Text on image is too long", 1


def check_link(url):
    try:
        response = req.get(url=url, timeout=5)
    except ConnectionError:
        return False, 1

    if response.ok:
        return True, 0
    else:
        return False, 1


def check_tags(text):
    tags = [el.replace("#", "") for el in re.findall(r"#[а-яА-Я@\w]+", text)]
    if len(tags) == 0 or len(tags) > 4:
        return "Bad count of tags (best between 2 and 4)", 2
    else:
        tags_info = {}
        points = 0
        for tag in tags:
            tag_info = util.parse_hashtag_stats(tag)
            tags_info[tag] = tag_info
            if int(re.findall(r"\d", tag_info)[0]) < 2:
                points += 1
        return tags_info, points


def perform_full_analysis(post):
    points = 0
    report = {}

    if "text" in post:
        orth_response = check_orthography(post["text"])
        report["text"] = orth_response[0]
        points += orth_response[1]

        tags_response = check_tags(post["text"])
        report["tags"] = tags_response[0]
        points += tags_response[1]

    if "images" in post:
        report["images"] = []
        for image in post["images"]:
            image_response = check_image(image["url"], image["width"], image["height"])
            report["images"].append(image_response[0])
            points += image_response[1]

    if "url" in post:
        link_response = check_link(post["url"])
        report["is_working_link"] = link_response[0]
        points += link_response[1]

    if points == 0:
        report["result"] = "excellent"
    elif 0 < points < 5:
        report["result"] = "acceptable"
    else:
        report["result"] = "bad"

    return report
