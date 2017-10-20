import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def get_all_users():
    r = requests.get(API_URL+'users')
    if r.status_code == 200:
        return 200, r.json()
    return r.status_code, []


def search_user(text_to_find):
    r = requests.get(API_URL + 'users/search/' + text_to_find)
    if r.status_code == 200:
        return 200, r.json()
    return r.status_code, []


def get_user(user_id):
    r = requests.get(API_URL + 'users/' + user_id)
    if r.status_code == 200:
        return 200, r.json()
    return r.status_code, []


def get_all_pots():
    r = requests.get(API_URL+'pots')
    if r.status_code == 200:
        return 200, r.json()
    return r.status_code, []


def get_pot(pot_id):
    if len(pot_id) > 0:
        r = requests.get(API_URL + 'pots/' + pot_id)
        if r.status_code == 200:
            return 200, r.json()
        return r.status_code, None
    return 404, None

