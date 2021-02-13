import os
import pickle


def get_user_list():
    list = os.listdir('./users')
    return list

def get_cookies(username):
    cookie_list = []
    for cookie in pickle.load(open(f'./users/{username}','rb')):
        cookie_list.append(cookie)
    return cookie_list

def save_cookies(cookies,username):
    pickle.dump(cookies,open(f'./users/{username}','wb'))
