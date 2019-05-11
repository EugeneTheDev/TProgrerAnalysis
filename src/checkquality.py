import re

import requests as req
from watson_developer_cloud.natural_language_understanding_v1 import EmotionOptions
from watson_developer_cloud.natural_language_understanding_v1 import Features
from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1
from watson_developer_cloud.watson_service import WatsonApiException

import util


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
    text = get_text_from_image(url)
    print(len(text))
    if not 50 < len(text) < 110:
        if 680 < width < 720 and 480 < height < 520:
            return "OK"
        else:
            return "Bad image size (700x500 is the best)"
    else:
        return "Text on image is too long"


def check_link(url):
    response = req.get(url=url)
    if response.ok:
        return True
    else:
        return False


def check_tags(text):
    print(re.findall(r"#[а-яА-Я@]+", text))


def get_text_from_image(url, language='rus'):
    payload = {'url': url,
               'apikey': "374e73777688957",
               "language": language
               }
    r = req.post('https://api.ocr.space/parse/image', data=payload)
    return r.json()["ParsedResults"][0]["ParsedText"]


def get_emotions(text):
    text = util.translate(text)
    text = f'<i>{text}</i>'
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='vcfJHb4lqz67pevf5vnqdOqVe-bOtFefMqUG5Q3c4ha2',
        url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
    )
    try:
        response = natural_language_understanding.analyze(
            html=text,
            features=Features(emotion=EmotionOptions())).get_result()
        return response["emotion"]["document"]["emotion"]
    except WatsonApiException:
        return "API error"
