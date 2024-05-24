import pygame
from scene import Scene
from loading import Loading
from input import InputBox, Button, Text
import requests
import json
from context import Context

class Menu(Scene):
    def __init__(self, width, height, host="localhost"):
        self.context = None
        self.width = width
        self.height = height 
        self.player_id = "P1"
        self.room_id = ""
        self.key = ""
        self.room_id_label = Text(100, 50, 200, 40, "Room id")
        self.input_room_id = InputBox(100, 100, 200, 36, lambda text : self.save_room_id(text))
        self.room_key_label = Text(100, 150, 200, 40, "Room key")
        self.input_key = InputBox(100, 200, 200, 36, lambda text : self.save_room_key(text))
        self.join_button = Button(100, 250, 250, 40, lambda : self.join_room(), text="Join a room")
        self.create_button = Button(100, 300, 250, 40, lambda : self.create_room(), text="Create room")
        self.host = host
    
    def save_room_id(self, inp):
        self.room_id = inp
        
    def save_room_key(self, inp):
        self.key = inp
       
    def create_room(self):
        print("Creating room...")
        r = requests.post(F"http://{self.host}/api/create_room")
        response = json.loads(r.content)
        print(F'Join with\nroomId = {response["id"]}\nkey = {response["key"]}')
        self.context = Context(response["id"], response["key"], response["user_id"], self.player_id, host=self.host)
        
    def join_room(self):
        r = requests.post(F"http://{self.host}/api/add_player/{self.room_id}/{self.key}")
        response = json.loads(r.content)
        self.context = Context(self.room_id, self.key, response["user_id"], response["player_id"], host=self.host)
        
    def reset(self):
        self.context = None

    def update(self):
        self.input_room_id.update()
        self.create_button.update()
        self.input_key.update()
        self.join_button.update()
    
    def display(self, screen : pygame.Surface):
        self.input_room_id.draw(screen)
        self.create_button.draw(screen)
        self.room_id_label.draw(screen)
        self.room_key_label.draw(screen)
        self.input_key.draw(screen)
        self.join_button.draw(screen)
    
    def ended(self):
        return self.context != None
    
    def transition(self) -> Scene:
        if not self.ended():
            return self
        return Loading(self.width, self.height, self.context, self)
    
    def event(self, event : pygame.event.Event) -> None:
        self.input_room_id.handle_event(event)
        self.create_button.handle_event(event)
        self.input_key.handle_event(event)
        self.join_button.handle_event(event)
        
    def quit(self) -> None:
        pass