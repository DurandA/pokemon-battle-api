import asyncio
from . import celery

from flask_socketio import SocketIO

socketio = SocketIO(message_queue='redis://')

print(__name__)

async def battle_events():
    for i in range(100):
        print('Worker async event %i' %i)
        socketio.emit('message',
                          {'data': 'Worker async event %i' %i},
                          namespace='/test')
        await asyncio.sleep(1)

@celery.task()
def broadcast_battle(battle_id):
    print('broadcasting battle...')
    event_loop = asyncio.get_event_loop()
    socketio.emit('message',
                      {'data': 'Worker generated event'},
                      namespace='/test')
    event_loop.run_until_complete(
        battle_events()
    )
