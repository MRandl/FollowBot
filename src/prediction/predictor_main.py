from joblib import dump, load
import pandas as pd
import tweepy
import numpy as np
import numpy.random as random
import os.path
import time
import pickle
from prediction.helpers import *

all_user_info = ['id', 'has_chain', 'has_wave', 'has_100', 'has_followback', 'has_corona', 'has_bot',
                 'has_invitation_link', 'last_known_screen_name', 'erate', 'friends', 'followers']
relevant_info_about_user = ['has_chain', 'has_wave', 'has_100', 'has_followback', 'has_corona', 'has_bot',
                            'has_invitation_link', 'erate', 'friends', 'followers']

mean = np.array(
    [0.001155, 0.008316, 0.077616, 0.163548, 0.000693, 0.013629, 0.088011, 0.678295, 3146.707323, 3175.801571]).reshape(1, 10)
std = np.array(
    [0.033970, 0.090823, 0.267597, 0.369908, 0.026319, 0.115958, 0.283344, 0.301506, 8518.075296, 8639.824506]).reshape(1, 10)


def calculateInfoUser(id, api):  # calculate all relevant info of a user; to use for the predictions
    try:
        followings = list(
            tweepy.Cursor(api.friends_ids, id=id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items())
    except tweepy.TweepError:
        time.sleep(60)
        return None
    try:
        followers = list(
            tweepy.Cursor(api.followers_ids, id=id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items())
    except tweepy.TweepError:
        time.sleep(60)
        return None
    time.sleep(60)
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
    with open('./prediction/model.pkl', 'rb') as f:
        predictor = pickle.load(f, encoding='utf-8')
    x = pd.DataFrame(columns=all_user_info)
    for id in ids:
        user_info = calculateInfoUser(id, api)
        if user_info is None:
            continue
        x = x.append(pd.Series(user_info, index=all_user_info), ignore_index=True)
    data = x.drop(axis=1, labels=['id', 'last_known_screen_name'])
    data = (data.to_numpy() - mean) / std
    predicted = list(map(lambda x : x[0] < 0.6, predictor.predict_proba(data)))
    x['predicted_followback'] = predicted
    ids_predicted = list(x[predicted].id)
    return x, ids_predicted


def check_followbacks(api):
    prediction_path = 'res/prediction.csv'
    if os.path.exists(prediction_path):
        prediction = pd.read_csv('./res/prediction.csv')
        users_ids = list(prediction.id)
        predicted_followbacks = list(prediction.predicted_followback)
        real_followbacks = []
        ids_followbacks = []
        user_id = api.me()
        try:
            followers = list(
                tweepy.Cursor(api.followers_ids, id=user_id, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True).items())
        except tweepy.TweepError:
            raise LookupError("An error occured; relaunch the program")

        for id in users_ids:
            try:
                user = api.get_user(id)
            except tweepy.TweepError:
                prediction = prediction[prediction.id != id]
                continue
            if id in followers:
                print(user.screen_name + " follows you back")
                real_followbacks.append(True)
                ids_followbacks.append(id)
            else:
                print(user.screen_name + " does not follows you back")
                real_followbacks.append(False)
        with open('./prediction/model.pkl','rb') as f:
            predictor = pickle.load(f,encoding='utf-8')
        data = prediction.drop(axis=1, labels=['id', 'last_known_screen_name', 'predicted_followback'])
        data = (data.to_numpy() - mean) / std
        for i in range(200):
            predictor.partial_fit(data,real_followbacks)
        with open('./prediction/model.pkl','wb') as f:
            pickle.dump(predictor,f)
        if len(ids_followbacks) > 0:
            try:
                choice = int(input(
                    "If you wish, we can propose to you some users to follow. Type 1 to accept, anything else to refuse : "))
            except ValueError:
                return None
            if choice == 1:
                print("We will propose to you at most 15 users, found using a BFS method (this may take some time). Some will be random; others will have a good followers/followings ratio ")
                id_user = ids_followbacks[0]
                followers = list(
                    tweepy.Cursor(api.followers_ids, id=id_user, wait_on_rate_limit=True,
                                  wait_on_rate_limit_notify=True).items(500))
                people_to_try = []
                for follower_id in random.choice(followers, 7):
                    try:
                        user = api.get_user(follower_id)  # to verify that the user still exists
                    except tweepy.TweepError:
                        continue
                    people_to_try.append(follower_id)
                count = 8
                for follower_id in followers:
                    if count == 0:
                        break
                    if follower_id in people_to_try:
                        continue
                    else:
                        try:
                            user = api.get_user(follower_id)
                        except tweepy.TweepError:
                            continue
                        if user.friends_count == 0:
                            continue
                        ratio = user.followers_count / user.friends_count
                        if ratio >= 0.90 and ratio <= 1:
                            count -= 1
                            people_to_try.append(follower_id)

                return people_to_try
            else:
                return None
        else:
            return None
