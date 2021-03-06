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


def update_plant(plant_id, new_name, new_hume_tie, new_hume_amb, new_temp_tie, new_temp_amb):
    payload = {
        'name': new_name,

        'maxTemp': new_temp_tie[1],
        'minTemp': new_temp_tie[0],

        'maxRoomTemp': new_temp_amb[1],
        'minRoomTemp': new_temp_amb[0],

        'maxHum': new_hume_amb[1],
        'minHum': new_hume_amb[0],

        'maxMoist': new_hume_tie[1],
        'minMoist': new_hume_tie[0],
    }
    r = requests.put(API_URL + "plants/" + plant_id, data=payload)
    return r.status_code


def update_plant_description(plant_id, new_description):
    payload = {'description': new_description}
    r = requests.put(API_URL + "plants/" + plant_id, data=payload)
    return r.status_code


def update_plant_category(plant_id, category_id, new_type, new_description):
    payload = {'type': new_type, 'description': new_description}
    r = requests.put(API_URL + "plants/" + plant_id + "/tips/" + category_id, data=payload)
    return r.status_code


def update_post_image(post_id, file_name):
    file = {'image': open(file_name, 'rb')}
    r = requests.put(API_URL+'posts/'+post_id, files=file)
    return r.status_code


def update_post_text(post_id, text):
    payload = {'text': text}
    r = requests.put(API_URL + "posts/"+post_id, data=payload)
    return r.status_code


def update_comment(post_id, comment_id, text):
    payload = {'text': text}
    r = requests.put(API_URL + "posts/" + post_id + "/comments/" + comment_id, data=payload)
    return r.status_code


def update_sale_image(sale_id, price, file_name, text, tags):
    payload = {'price': price, 'text': text, 'tags': tags.replace(" ", "")}
    file = {'image': open(file_name, 'rb')}
    r = requests.put(API_URL + "posts/"+sale_id, data=payload, files=file)
    return r.status_code


def update_sale(sale_id, price, text, tags):
    payload = {'price': price, 'text': text, 'tags': tags.replace(" ", "")}
    r = requests.put(API_URL + "posts/"+sale_id, data=payload)
    return r.status_code
