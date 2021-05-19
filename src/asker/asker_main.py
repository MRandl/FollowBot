import os.path
import tweepy

def get_api():
  password_path = 'res/init/login.txt'
  if(os.path.exists(password_path)):
    passwords = open(password_path, 'r').read().splitlines()
    keys = [passwords[i] for i in range(4)]

  else:
    os.makedirs(os.path.dirname(password_path), exist_ok=True)
    password_file = open(password_path, 'w')
    key_names = ['oauth login', 'oauth password', 'public access token', 'private access token']
    keys = []
    for index in range(len(key_names)):
      element = input('\nPlease input your ' + key_names[index] + ':\n')
      keys.append(element)
      password_file.write(element + '\n')
    password_file.close()
    print('')

  auth = tweepy.OAuthHandler(keys[0], keys[1])
  auth.set_access_token(keys[2], keys[3])
  return tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def get_list_followings():
  bfs_path = 'res/init/bfs.txt'
  if(os.path.exists(bfs_path)):
    return open(bfs_path, 'r').read().splitlines()
  
  else:
    os.makedirs(os.path.dirname(bfs_path), exist_ok=True)
    bfs_file = open(bfs_path, 'w')
    
    ids_path = input('\nPlease enter the inital ids path : \n')
    ids = open(ids_path, 'r').read().splitlines()
    for elem in ids:
      bfs_file.write(elem + '\n')
    bfs_file.close()
    return ids


def calculateInfoUser(id, api): #calculate all relevant info of a user; to use for the predictions
  try:
    followings = list(tweepy.Cursor(api.friends_ids, id = id, wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items())
  except tweepy.TweepError:
    return None
  try:
    followers = list(tweepy.Cursor(api.followers_ids, id = id, wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items())
  except tweepy.TweepError:
    return None
  intersection = list(set(followers) & set(followings))
  union = list(set(followers) | set(followings))
  if(len(union) == 0):
    erate = 0
  else:
    erate = len(intersection)/len(union)
  return (id,len(followings),len(followers),erate)

