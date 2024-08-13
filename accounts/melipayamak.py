import requests
from random import randint


def send_token(number):
    code = randint(100000, 999999)
    args = [str(code)]
    data = {'bodyId': 237640, 'to': number, 'args': args}
    response = requests.post('https://console.melipayamak.com/api/send/shared/9a2644807e4e4288b1a2f9dbc7c9fd24', json=data)
    x = response.json()
    if x["status"] and x["recId"]:
        return {"code":str(code), "status":x["status"], "recid":x["recId"]}
    return None

def send_sms(number, bodyId, args):
    data = {'bodyId': bodyId, 'to': number, 'args': args}
    response = requests.post('https://console.melipayamak.com/api/send/shared/9a2644807e4e4288b1a2f9dbc7c9fd24', json=data)
    return response.json()