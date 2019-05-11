import re

import requests as req

import util


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
    print(len(text))
    if not 50 < len(text) < 110:
        if 680 < width < 720 and 480 < height < 520:
            return "OK", 0
        else:
            return "Bad image size (700x500 is the best)", 1
    else:
        return "Text on image is too long", 1


def check_link(url):
    response = req.get(url=url)
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

