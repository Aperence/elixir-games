import time
from typing import Tuple, List
from context import Context
import argparse
import requests

explosion_time = 3
explosion_effect_duration = 0.5
invicibility_time = 1.5
ending_screen_time = 5

class BombermanServer:
    def __init__(self, room_id, key, user_id, host):
        self.context = Context(room_id, key, user_id, "", host=host)
        requests.post(F"http://{host}/api/server_ready/{room_id}/{key}/{user_id}")
        self.player_healths = {
            i : 3 for i in range(4)
        }
        self.player_invincibility = {
            i : -1 for i in range(4)
        }
        self.map = [
            ["", "", "", "", "", "", ""],
            ["", "X", "X", "", "X", "X", ""],
            ["", "X", "", "", "", "X", ""],
            ["", "", "", "", "", "", ""],
            ["", "X", "", "", "", "X", ""],
            ["", "X", "X", "", "X", "X", ""],
            ["", "", "", "", "", "", ""]
        ]
        self.bombs : List[Tuple[int, int, int]] = []
        self.player_positions = {
            0 : (0, 0),
            1 : (0, 6),
            2 : (6, 0),
            3 : (6, 6),
        }
        self.ended_time = None
        self.winner = None
        self.explosions = []
        self.n = len(self.map)
        self.m = len(self.map[0])
        

    def update(self) -> None:
        now = time.time()
        for (x, y, time_bomb) in self.bombs:
            if (now > time_bomb + explosion_time):
                self.explode(x, y, time_bomb)  
        count_alive = 0
        alive = None
        for (player, health) in self.player_healths.items():
            if (health != 0):
                count_alive += 1
                alive = player
   
        if (self.winner == None and count_alive <= 1):
            self.ended_time = time.time()
            self.winner = alive if alive != None else "None"
            self.context.send_message("winner", {"player" : alive})

    def put_bomb(self, player_id):
        (x, y) = self.player_positions[player_id]
        self.bombs.append((x, y, time.time()))
        self.context.send_message("new_bomb", {"x" : x, "y" : y})
    
    def dist(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)
    
    def is_invincible(self, player_id):
        now = time.time()
        return now <= self.player_invincibility[player_id] + invicibility_time
    
    def take_damage(self, player_id):
        if not self.is_invincible(player_id) and self.player_healths[player_id] > 0:
            self.player_healths[player_id] = self.player_healths[player_id] - 1
            self.player_invincibility[player_id] = time.time()
            self.context.send_message("player_damaged", {"player" : player_id})
    
    def explode(self, x : int, y : int, time_bomb : int) -> None:
        if not (x, y, time_bomb) in self.bombs:
            return
        self.bombs.remove((x, y, time_bomb))
        self.context.send_message("bomb_exploded", {"x" : x, "y" : y })
        for (off_x, off_y) in [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 0)]:
            for (player, pos) in self.player_positions.items():
                if ((x+off_x, y+off_y) == pos):
                    self.take_damage(player)
        for (x2, y2, time2) in self.bombs:
            if self.dist(x, y, x2, y2) <= 1:
                self.explode(x2, y2, time2)
                
    def bomb_at(self, x : int, y : int) -> bool:
        for (x_b, y_b, _) in self.bombs:
            if (x_b == x and y_b == y):
                return True
        return False
    
    def valid_move(self, player_id, x, y):
        x_prev, y_prev = self.player_positions[player_id]
        return x in range(0, self.n) \
            and y in range(0, self.m) \
            and self.map[x][y] == "" \
            and not self.bomb_at(x, y) \
            and not (x, y) in self.player_positions.values() \
            and self.player_healths[player_id] != 0 \
            and self.dist(x_prev, y_prev, x, y) <= 1
        
    def move(self, player_id : str, x_off : int, y_off : int) -> None:
        if (x_off == 0 and y_off == 0):
            return
        (x, y) = self.player_positions[player_id]
        if self.valid_move(player_id, x+x_off, y+y_off):
            self.player_positions[player_id] = (x+x_off, y+y_off); 
            self.context.send_message("new_pos", {"player" : player_id, "x" : x+x_off, "y" : y + y_off})
       
    def ended(self):
        return self.ended_time != None and time.time() > self.ended_time + ending_screen_time 
    
    def receive(self):
        # move/put bomb
        msg = self.context.get_message()
        if (msg == None):
            return
        print(msg)
        topic = msg[3]
        params = msg[4]
        if (topic == "ask_put_bomb"):
            self.put_bomb(params["player_id"])
        if (topic == "ask_move"):
            self.move(params["player_id"], params["x_off"], params["y_off"])
            
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str)
    parser.add_argument("--room-id", type=str)
    parser.add_argument("--user-id", type=str)
    parser.add_argument("--host", type=str, default="localhost:4000")
    
    args = parser.parse_args()
    
    print(F"Host = {args.host}")
    state = BombermanServer(args.room_id, args.key, args.user_id, args.host)
    
    while (not state.ended()):
        state.receive()
        state.update()
        
if __name__ == "__main__":
    main()