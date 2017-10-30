import requests


API_URL = 'http://smartcrop.lightup.cl/api/'


def delete_plant_tip(plant_id, tip_id):
    r = requests.delete(API_URL + 'plants/' + plant_id + '/tips/' + tip_id)
    return r.status_code
