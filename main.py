import asker_main
import predictor_main
# 1
api = asker_main.get_api()
print(api)
# 2
asker_main.ask_for_initial_followings()

# 3
predictor_main.predict(['BarackObama'])

# todo 4 