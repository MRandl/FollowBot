import asker.asker_main as asker_main
import prediction.predictor_main as predictor_main

def ask_followings(potential_advised_followings = None):
    if potential_advised_followings is None:
        followings_id = asker_main.get_list_followings(api)
        if followings_id is None:
            raise ValueError("You choose to follow nobody today; goodbye!")
    else:
        followings_id = potential_advised_followings
    df, potential_followers = predictor_main.predict_users_who_followback(followings_id, api)
    if len(potential_followers) == 0:
        print("No one was predicted to follow you back; try again with other names")
        ask_followings()
    else:
        print("Users we believe are likely to followack: ")
        for id in potential_followers:
            user = api.get_user(id)
            print(user.screen_name)
        print("You can always try following the others, we simply don't think they will followback.")
        print("All users are in the prediction.csv file in the res directory.")
        df.to_csv("./res/prediction.csv", index=False)

print("Welcome to Followbot")
# 1
api = asker_main.get_api()
# 2
potential_advised_followings = predictor_main.check_followbacks(api)

ask_followings(potential_advised_followings)

print("Come back in a week or so and rerun the program to check who followed you back, and to train the model on this new data")