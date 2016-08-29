from flask_socketio import emit


def async_test(message):
    emit('echo', message)
