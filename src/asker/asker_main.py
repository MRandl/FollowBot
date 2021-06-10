import os.path
import tweepy


def get_api():
    password_path = 'res/init/login.txt'
    if (os.path.exists(password_path)):
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
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def ask_number_followings(warn = ""):
    if warn != "":
      print(warn)
    try:
      count = int(input("Please enter the number of people you wish to follow today; we advise no more than 15, and it has to be less than 50 : "))
    except ValueError:
      return ask_number_followings()
    if count > 50 or count < 0:
      return ask_number_followings("Enter a valid number")
    elif count == 0:
        return -1
    return count

def get_list_followings(api):
    first_ids = 'res/init/ids_followings.txt'
    if os.path.exists(first_ids):
        f = open(first_ids, 'r')
        ids = f.read().splitlines()
        f.close()
        return ids
    else:
        potential_followings = []
        count = ask_number_followings()
        if count == -1:
            return None
        while count > 0:
            screen_name = input("Type the screen name of someone you're thinking of following (it's the name next to the @) : ")
            try:
              user = api.get_user(screen_name)
              potential_followings.append(user.id)
              count -= 1
            except tweepy.TweepError:
              print("The given user doesn't exist; type another")
        return potential_followings



