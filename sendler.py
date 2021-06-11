import requests

name = input('Введите имя: ')

while True:
    text = input()
    response = requests.post(
        url='http://127.0.0.1:5000/send',
        json={'name': name, 'text': text}
        #json={'name': {}, 'text': {}}
        #json={'name': 'Jack'}
        #json={}
        #json='23565'
    )
