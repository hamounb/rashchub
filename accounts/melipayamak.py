import requests


def send_token(number):
    data = {'to': number}
    response = requests.post('https://console.melipayamak.com/api/send/otp/9a2644807e4e4288b1a2f9dbc7c9fd24', json=data)
    return response.json()