from watson_developer_cloud.natural_language_understanding_v1 import EmotionOptions
from watson_developer_cloud.natural_language_understanding_v1 import Features
from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1
from watson_developer_cloud.watson_service import WatsonApiException

from src import util


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
