import pygame
from scene import Scene
import bomberman
from context import Context
from input import Text
import time
import requests
import json

number_players=1
interval_status = 3 # every 3s, ask state of game

class Loading(Scene):
    def __init__(self, width : int, height : int, context : Context, menu):
        self.menu = menu
        self.width = width
        self.height = height 
        self.context = context
        self.number_players = 1
        self.server_ready = False
        self.room_id = Text(100, 100, width-200, 40, F"Room id = {self.context.room_id}")
        self.room_key = Text(100, 200, width-200, 40, F"Room key = {self.context.key}")
        self.number_players_label = Text(100, 300, width-200, 40, F"{self.number_players}/{number_players} players in room")
        self.server_ready_label = Text(100, 400, width-200, 40, F"Server is {'' if self.server_ready else 'not'} ready")
        self.last_time_query = -1
        
    def reset(self):
        pass

    def update(self):
        now = time.time()
        if (now > self.last_time_query + interval_status):
            self.last_time_query = now
            r = requests.get(F"http://{self.context.host}/api/state_room/{self.context.room_id}")
            response = json.loads(r.content)
            if (response["status"] != "ok"):
                return
            self.server_ready = response["server_ready"]
            self.number_players = response["nb_players"]
    
    def display(self, screen : pygame.Surface):
        self.room_id.draw(screen)
        self.room_key.draw(screen)
        self.number_players_label.draw(screen)
        self.server_ready_label.draw(screen)
    
    def ended(self):
        return self.number_players == number_players and self.server_ready
    
    def transition(self) -> Scene:
        if not self.ended():
            return self
        return bomberman.Bomberman(self.width, self.height, self.menu, self.context)
    
    def event(self, event : pygame.event.Event) -> None:
        pass
        
    def quit(self) -> None:
        pass