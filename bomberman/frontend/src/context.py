import channel_client

class Context:
    def __init__(self, room_id : str, key : str, user_id : str, player_id : str, host="localhost:4000"):
        self.room_id = room_id
        self.key = key
        self.user_id = user_id
        self.player_id = player_id
        self.socket = channel_client.connect_socket(
            F"ws://{host}/bomberman/websocket?vsn=2.0.0"
        )
        self.host = host
        self.lobby = f"room:{room_id}"
        channel_client.join_lobby(self.socket, self.lobby, params={"user_id" : user_id})
        
    def send_message(self, type, params):
        params["user_id"] = self.user_id
        channel_client.send_message(self.socket, self.lobby, type, params)
        
    def get_message(self):
        return channel_client.get_message(self.socket)