from src import util


def likes_analysis(likes):
    res = analyze_values(likes)
    if res > 0:
        return "Wow! Seems like this post was very cool"
    elif res < 0:
        return "Oh... This post wasn`t so good"
    else:
        return ""


def comments_analysis(comments):
    res = analyze_values(comments)
    if res > 0:
        return "How many comments!"
    elif res < 0:
        return "There is less comments then was excepted"
    else:
        return ""


def emotions_analysis(comments_text):
    emotions = util.get_emotions(comments_text)
    # noinspection PyTypeChecker
    result = 0.5 * emotions["joy"] - 0.15 * emotions["sadness"] - 0.1 * emotions["fear"] \
        - 0.05 * emotions["disgust"] - 0.2 * emotions["anger"]
    return "Positive" if result >= 0 else "Negative"


def perform_full_prediction(post):
    report = {}

    likes_response = likes_analysis(post["likes"])
    report["likes"] = {
        "send": likes_response == "",
        "message": likes_response
    }

    comments_response = comments_analysis(post["comments"])
    report["comments"] = {
        "send": comments_response == "",
        "message": comments_response
    }

    emotions_response = emotions_analysis(post["comments_text"])
    report["emotions"] = {
        "send": comments_response == "",
        "message": emotions_response
    }
    return report


def analyze_values(values):
    length = len(values)
    mid = sum(values)/length
    dispersion = sum([(value-mid)**2 for value in values])/length
    o = dispersion**0.5
    present_o = mid - values[-1]
    if o < abs(present_o):
        if present_o < 0:
            return 1
        else:
            return -1
    else:
        return 0



