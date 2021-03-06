import boto3
import requests as req
from bs4 import BeautifulSoup
from watson_developer_cloud.natural_language_understanding_v1 import EmotionOptions
from watson_developer_cloud.natural_language_understanding_v1 import Features
from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1
from watson_developer_cloud.watson_service import WatsonApiException

from src import credentials as cr

rekognition = boto3.client("rekognition", aws_access_key_id=cr.KEY_ID,
                           aws_secret_access_key= cr.ACCESS_KEY,
                           region_name="eu-west-1")



def translate(text):
    response = req.get(url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t", params={
        "q": text
    }, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    })
    return response.json()[0][0][0]


def get_text_square_from_image(url):
    response = req.get(url)

    if response.ok:
        result = rekognition.detect_text(
            Image={
                "Bytes": response.content
            }
        )
        square = 0
        for label in result["TextDetections"]:
            square += label["Geometry"]["BoundingBox"]["Width"] * label["Geometry"]["BoundingBox"]["Height"]
        return square
    return 0


def parse_hashtag_suggestion(text):
    response = req.post(url="https://ritekit.com/api-demo/hashtag-suggestions", data={
        "topic": text,
        "_do": "apiDemo-form-submit",
        "_submit": "Show hashtag suggestions"
    })
    soup = BeautifulSoup(response.text, "html.parser")
    return [el.find("td").get_text() for el in soup.find("div", class_="table-responsive").find_all("tr")[1:]]


def get_emotions(text):
    text = translate(text)
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