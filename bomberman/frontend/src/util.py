import requests
import json
from context import Context

url = "http://127.0.0.1:4000"

def join_room(roomId, key):
    r = requests.get(F"{url}/api/add_player/{roomId}/{key}")
    response = json.loads(r.content)
    print(response)
    c = Context(roomId, key, response["user_id"], response["player_id"])
    
roomId = "5cdd49f2-42b7-4362-a22f-c71c8c49c65f"
key = "f4d0c8a6-431e-4b69-9110-d60c9f607167"
join_room(roomId, key)