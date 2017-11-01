import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def delete_plant_tip(plant_id, tip_id):
    r = requests.delete(API_URL + 'plants/' + plant_id + '/tips/' + tip_id)
    return r.status_code


def delete_comment(post_id, comment_id):
    r = requests.delete(API_URL + 'posts/' + post_id + '/comments/' + comment_id)
    return r.status_code


def delete_post(post_id):
    r = requests.delete(API_URL + 'posts/' + post_id)
    return r.status_code
