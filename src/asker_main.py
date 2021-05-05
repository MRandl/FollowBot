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

def get_list_followings(api):
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
    
    return ids