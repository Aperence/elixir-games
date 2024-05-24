from websockets.sync.client import connect
import json


def join_lobby(socket, lobby_name, params={}):
    socket.send(f'["0", "0", "{lobby_name}", "phx_join", {json.dumps(params)}]')
    message = socket.recv()
    message = json.loads(message)
    if message[4]["status"] != "ok":
        raise ConnectionError("Failed to join lobby")


def send_message(socket, lobby_name, type, params={}):
    socket.send(f'[null, "3", "{lobby_name}", "{type}", {json.dumps(params)}]')


def get_message(socket):
    try:
        return json.loads(socket.recv(0))
    except:
        return None


def connect_socket(uri):
    return connect(uri)


def disconnect_socket(socket):
    socket.close()
