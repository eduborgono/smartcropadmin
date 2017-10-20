import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def update_user_pass(userid, password):
    pass


def update_user_nick(user_id, nick):
    payload = {"nickname": nick}
    r = requests.put(API_URL+"users/"+user_id, data=payload)
    return r.status_code


def update_user_name(user_id, name):
    payload = {"name": name}
    r = requests.put(API_URL+"users/"+user_id, data=payload)
    return r.status_code


def update_profile(user_id, file_name):
    file = {'avatar': open(file_name, 'rb')}
    r = requests.put(API_URL+'users/'+user_id, files=file)
    return r.status_code


def update_pot_owner(pot_id, user_id):
    payload = {"owner": user_id}
    r = requests.put(API_URL + "pots/" + pot_id, data=payload)
    return r.status_code


def update_pot_name(pot_id, new_name):
    payload = {"name": new_name}
    r = requests.put(API_URL + "pots/" + pot_id, data=payload)
    return r.status_code

