import numpy as np
from watson_developer_cloud.natural_language_understanding_v1 import EmotionOptions
from watson_developer_cloud.natural_language_understanding_v1 import Features
from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1
from watson_developer_cloud.watson_service import WatsonApiException

from src import util


# {'sadness': 0.494259, 'joy': 0.012937, 'fear': 0.09078, 'disgust': 0.36141, 'anger': 0.388772} - commentary/emotions
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


def likes_analysis(likes, members, previous):
    data = [el["likes_count"] / el["members_count"] for el in previous]
    data.append(likes/members)
    z = np.polyfit(np.arange(0, len(data)), np.array(data), 1)
    return "Growing" if z[0] > 0 else "Falling", z[0]


def emotions_analysis(comments_text, commentary):
    emotions = get_emotions(comments_text)
    emotions_data = commentary + emotions

    sadness_data = [el["sadness"] for el in emotions_data]




print(likes_analysis(886, 261_453, [
    {"members_count": 261_437, "likes_count": 456},
    {"members_count": 261_400, "likes_count": 768},
    {"members_count": 261_370, "likes_count": 945},
    {"members_count": 261_320, "likes_count": 567}
]))