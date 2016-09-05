from app.extensions import celery, socketio

from app.modules.battles.models import Battle
from app.modules.battles.schemas import DetailedBattleSchema

from flask_socketio import SocketIO

from io import StringIO
import requests
import time
import re


@celery.task()
def broadcast_battle(battle_id, battle):
    payload = {}

    # r = requests.get("http://127.0.0.1:5000/api/v1/battles/{0}".format(battle_id))
    # battle = r.json()

    # for tkey in ['team1', 'team2']:
    #     team = battle[tkey]
    #     for pokemon in team['pokemons']:
    #         payload['%s[]' % tkey] = pokemon['id']

    r = requests.post("http://127.0.0.1:4000/fight", json=battle)
    finished = False
    result = StringIO(r.text)

    for line in result:
        event = line.strip()
        if event:
            print(event)
            socketio.send(event, namespace='/battles/{0}'.format(battle_id))
            match = re.match('(.*?) defeated (.*?)!', event)
            if match:
                winner = match.group(1)
                print('%s won!' % winner)
                print(battle)
                r = requests.put("http://127.0.0.1:5000/api/v1/battles/{}/outcome".format(battle_id), json={"trainer": winner})
            time.sleep(1)
    return winner
