import requests

trainers = [
    {"country_code":"JPN","gender":"male","name":"Ash Ketchum"},
    {"country_code":"JPN","gender":"female","name":"Serena"},
    {"country_code":"JPN","gender":"female","name":"Misty"},
    {"country_code":"JPN","gender":"female","name":"Jessie"},
    {"country_code":"JPN","gender":"female","name":"May"},
    {"country_code":"JPN","gender":"male","name":"Alain"},
    {"country_code":"JPN","gender":"male","name":"James"},
    {"country_code":"JPN","gender":"male","name":"Red"},
    {"country_code":"JPN","gender":"male","name":"Brock"},
    {"country_code":"JPN","gender":"female","name":"Dawn"},
    {"country_code":"JPN","gender":"male","name":"Gary Oak"},
    {"country_code":"JPN","gender":"male","name":"Clermont"},
    {"country_code":"JPN","gender":"female","name":"Bonnie"},
    {"country_code":"JPN","gender":"female","name":"Iris"},
    {"country_code":"JPN","gender":"male","name":"Lysandre"},
]

for trainer in trainers:
    r = requests.post('http://localhost:8080/api/v1/trainers/', json=trainer)
    print(r.status_code)
