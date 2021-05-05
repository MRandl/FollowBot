import asker_main
import predictor_main
# 1
api = asker_main.get_api()
# 2
followings_id = asker_main.get_list_followings()
print(followings_id)
# 3
predictor_main.predict(['BarackObama'])

