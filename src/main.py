import asker.asker_main as asker_main
import prediction.predictor_main as predictor_main

def ask_followings():
    followings_id = asker_main.get_list_followings(api)
    df, potential_followers = predictor_main.predict_users_who_followback(followings_id, api)
    if len(potential_followers) == 0:
        print("No one was predicted to follow you back; try again with other names")
        ask_followings()
    else:
        print("Users to follow: ")
        for id in potential_followers:
            user = api.get_user(id)
            print(user.screen_name)
        df.to_csv("./res/prediction.csv", index=False)

print("Welcome to followbot")
# 1
api = asker_main.get_api()
# 2
predictor_main.check_followbacks(api)
# 3
"""potential_followers = predictor_main.predict_users_who_followback(followings_id,api)
print("Users to follow: ")
for id in potential_followers:
    user = api.get_user(id)
    print(user.screen_name)"""

ask_followings()
print("Come back in a week or so and rerun the program to check who followed you back, and to train the model on this new data")