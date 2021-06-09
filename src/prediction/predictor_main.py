from joblib import dump, load
import pandas as pd
import tweepy
import os.path

from prediction.helpers import *

all_user_info = ['id', 'has_chain', 'has_wave', 'has_100', 'has_followback', 'has_corona', 'has_bot',
                 'has_invitation_link', 'last_known_screen_name', 'erate', 'friends', 'followers']
relevant_info_about_user = ['has_chain', 'has_wave', 'has_100', 'has_followback', 'has_corona', 'has_bot',
                            'has_invitation_link', 'erate', 'friends', 'followers']


def calculateInfoUser(id, api):  # calculate all relevant info of a user; to use for the predictions
    try:
        followings = list(
            tweepy.Cursor(api.friends_ids, id=id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items())
    except tweepy.TweepError:
        return None
    try:
        followers = list(
            tweepy.Cursor(api.followers_ids, id=id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items())
    except tweepy.TweepError:
        return None
    intersection = list(set(followers) & set(followings))
    union = list(set(followers) | set(followings))
    if len(union) == 0:
        erate = 0
    else:
        erate = len(intersection) / len(union)
    try:
        user = api.get_user(id=id)
    except tweepy.TweepError:
        return None
    return check_usr(user, id, erate)


def predict_users_who_followback(ids, api):
    predictor = load('./prediction/saved.bin')  # get back from file
    x = pd.DataFrame(columns=all_user_info)
    for id in ids:
        user_info = calculateInfoUser(id, api)
        if user_info is None:
            continue
        x = x.append(pd.Series(user_info, index=all_user_info), ignore_index=True)
    predicted = predictor.predict(x.drop(axis=1, labels=['id', 'last_known_screen_name']))
    x['predicted_followback'] = predicted
    ids_predicted = list(x[predicted].id)
    return x, ids_predicted


def check_followbacks(api):
    prediction_path = 'res/prediction.csv'
    if (os.path.exists(prediction_path)):
        prediction = pd.read_csv('./res/prediction.csv')
        users_ids = list(prediction.id)
        predicted_followbacks = list(prediction.predicted_followback)
        real_followbacks = []
        user_id = api.me()
        try:
            followers = list(
                tweepy.Cursor(api.followers_ids, id=user_id, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True).items())
        except tweepy.TweepError:
            raise LookupError("An error occured; relaunch the program")

        for id in users_ids:
            user = api.get_user(id)
            if id in followers:
                print(user.screen_name + " follows you back")
                real_followbacks.append(True)
            else:
                print(user.screen_name + " does not follows you back")
                real_followbacks.append(False)
        predictor = load('./prediction/saved.bin')  # get back from file
        predictor.partial_fit(prediction.drop(axis = 1, labels=['id', 'last_known_screen_name','predicted_followback']),real_followbacks)
        dump(predictor, './prediction/saved.bin')
