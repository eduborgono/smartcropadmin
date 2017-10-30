import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def new_user_acc(email, name, password, nickname):
    payload = {"email": email, "name": name, "password": password, "nickname": nickname}
    r = requests.post(API_URL + "signup", data=payload)
    return r.status_code


def new_pot():
    payload = {}
    r = requests.post(API_URL + "pots", data=payload)
    return r.status_code


def new_plant():
    payload = {}
    r = requests.post(API_URL + "plants", data=payload)
    return r.status_code


def new_plant_tip(plant_id, new_type, new_description):
    payload = {'type': new_type, 'description': new_description}
    r = requests.post(API_URL + "plants/" + plant_id + "/tips", data=payload)
    return r.status_code
