import asker.asker_main as asker_main
import prediction.predictor_main as predictor_main
# 1
api = asker_main.get_api()
# 2
followings_id = asker_main.get_list_followings(api)
# 3
predictor_main.predict(followings_id)

