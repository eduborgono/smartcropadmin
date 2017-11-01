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


def new_comment(post_id, user_id, text):
    payload = {'author': user_id, 'text': text}
    r = requests.post(API_URL + "posts/" + post_id + "/comments", data=payload)
    return r.status_code


def new_post(author_id, text):
    payload = {'author': author_id, 'type': 'social', 'mode': 'public', 'text': text}
    r = requests.post(API_URL + "posts", data=payload)
    return r.status_code


def new_post_image(author_id, file_name, text):
    payload = {'author': author_id, 'type': 'social', 'mode': 'public', 'text': text}
    file = {'image': open(file_name, 'rb')}
    r = requests.post(API_URL + "posts", data=payload, files=file)
    return r.status_code


def new_sale(author_id, price, text, tags):
    payload = {'author': author_id, 'type': 'sale', 'price': price, 'text': text, 'tags': tags.replace(" ", "")}
    r = requests.post(API_URL + "posts", data=payload)
    return r.status_code


def new_sale_image(author_id, price, file_name, text, tags):
    payload = {'author': author_id, 'type': 'sale', 'price': price, 'text': text, 'tags': tags.replace(" ", "")}
    file = {'image': open(file_name, 'rb')}
    r = requests.post(API_URL + "posts", data=payload, files=file)
    return r.status_code
