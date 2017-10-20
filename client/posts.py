import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def new_user_acc(email, name, password, nickname):
    payload = {"email": email, "name": name, "password": password, "nickname": nickname}
    r = requests.post(API_URL + "signup", data=payload)
    print(r.status_code)
    return r.status_code