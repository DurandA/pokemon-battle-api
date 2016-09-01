from . import celery

from flask_socketio import SocketIO

from app.modules.battles.models import Battle
from app.modules.battles.schemas import DetailedBattleSchema

from io import StringIO
import requests
import time
import re


socketio = SocketIO(message_queue='redis://')


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
            socketio.send(event, namespace='/battles/{0}'.format(battle_id))
            match = re.match('(.*?) defeated (.*?)!', event)
            if match:
                print('%s won!' % match.group(1))
            time.sleep(1)
