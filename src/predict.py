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
    if previous:
        data = [el["likes_count"] / el["members_count"] for el in previous]
        data.append(likes / members)
        z = np.polyfit(np.arange(0, len(data)), np.array(data), 1)
        return ("Growing", 0) if z[0] > 0 else ("Falling", -z[0]*10000)
    else:
        return "We need at least two posts data to perform analysis", 0


def emotions_analysis(comments_text):
    emotions = get_emotions(comments_text)
    # noinspection PyTypeChecker
    result = 0.5 * emotions["joy"] - 0.15 * emotions["sadness"] - 0.1 * emotions["fear"] \
        - 0.05 * emotions["disgust"] - 0.2 * emotions["anger"]
    return ("Positive", 0, emotions) if result > 0 else ("Negative", -result*15 + 0.1, emotions)


def perform_full_prediction(info):
    report = {}
    points = 0

    likes_response = likes_analysis(info["likes_count"], info["members_count"], info["previous"])
    report["likes"] = likes_response[0]
    points += likes_response[1]

    emotions_response = emotions_analysis(info["comments_text"])
    report["emotions"] = {}
    report["emotions"]["percentage"] = emotions_response[2]
    report["emotions"]["type"] = emotions_response[0]
    points += emotions_response[1]

    if points == 0:
        report["result"] = "excellent"
    elif 0 < points <= 1:
        report["result"] = "acceptable"
    else:
        report["result"] = "bad"

    print(points, emotions_response[1], likes_response[1])

    return report




