from context import Context
import pygame
import time
from typing import Tuple, List
from scene import Scene
import os

line_color = (0, 0, 0)

explosion_time = 3
explosion_effect_duration = 0.5
invicibility_time = 1.5
ending_screen_time = 5

base_path = os.path.dirname(__file__)
bomb_path = os.path.join(base_path, "../assets/bomb.png")
explosion_path = os.path.join(base_path, "../assets/explosion.png")

class Bomberman(Scene):
    def __init__(self, width, height, menu, context : Context):
        self.menu = menu
        self.context = context
        self.width = width
        self.height = height
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
        self.bombs : List[Tuple[int, int]] = []
        self.player_positions = {
            0 : (0, 0),
            1 : (0, 6),
            2 : (6, 0),
            3 : (6, 6),
        }
        self.colors = {
            0 : (255, 0, 0),
            1 : (0, 255, 0),
            2 : (0, 0, 255),
            3 : (255, 255, 0),
            "" : (255, 255, 255),
            "X" : (0, 0, 0)
        }
        self.ended_time = None
        self.winner = None
        self.explosions = []
        self.n = len(self.map)
        self.m = len(self.map[0])
        
    def quit(self) -> None:
        #self.network.disconnect()
        pass

    def update(self) -> None:
        #self.network.check_play()
        now = time.time()
        for (x, y, exp_time) in self.explosions:
            if (now > exp_time + explosion_effect_duration):
                self.explosions.remove((x, y, exp_time))
        msg = self.context.get_message()
        if (msg == None):
            return
        type = msg[3]
        payload = msg[4]
        if (type == "new_pos"):
            self.player_positions[payload["player"]] = (payload["x"], payload["y"])
        if (type == "winner"):
            self.winner = payload["player"]
            self.ended_time = now
        if (type == "new_bomb"):
            self.bombs.append((payload["x"], payload["y"]))
        if (type == "player_damaged"):
            self.player_healths[payload["player"]] -= 1
            self.player_invincibility[payload["player"]] = now
        if (type == "bomb_exploded"):
            self.bombs.remove((payload["x"], payload["y"]))
            self.add_explosion(payload["x"], payload["y"])
     
    def valid_pos_explosion(self, x, y):
        return x in range(self.n) and y in range(self.m) and self.map[x][y] == ""
       
    def add_explosion(self, x, y):
        for (x_off, y_off) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if self.valid_pos_explosion(x+x_off, y+y_off):
                self.explosions.append((x+x_off, y+y_off, time.time()))
    
    def event(self, event : pygame.event.Event):
        type = event.type
        if (type != pygame.KEYDOWN):
            return
        key = event.key
        offset = (0, 0)
        if key == pygame.K_z:
            offset = (0, -1)
        if (key == pygame.K_s):
            offset = (0, 1)
        if (key == pygame.K_q):
            offset = (-1, 0)
        if (key == pygame.K_d):
            offset = (1, 0)
        if (key == pygame.K_SPACE):
            self.context.send_message("ask_put_bomb", {})
        if (offset != (0, 0)):
            self.context.send_message("ask_move", {"x_off" : offset[0], "y_off" : offset[1]})
    
    def is_invincible(self, player_id):
        now = time.time()
        return now <= self.player_invincibility[player_id] + invicibility_time
       
    def ended(self):
        return self.ended_time != None and time.time() > self.ended_time + ending_screen_time 

    def display(self, screen : pygame.Surface) -> None:
        tile_width = self.width / self.m
        tile_height = self.height / self.n
             
        font = pygame.font.Font(pygame.font.get_default_font(), 36)   
        # Display the normal tiles
        for i in range(self.n):
            for j in range(self.m):
                color = self.colors[self.map[i][j]]
                pygame.draw.rect(screen, color, pygame.Rect(i*tile_width, j*tile_height, tile_width*1.01, tile_height*1.01))
         
        # Display the players and their health
        for (player, (x, y)) in self.player_positions.items():
            color = self.colors[player]
            pygame.draw.rect(screen, color, pygame.Rect(x*tile_width, y*tile_height, tile_width*1.01, tile_height*1.01))

            health = str(self.player_healths[player])
            if self.is_invincible(player) and health != "0":
                health += "*"
            text = font.render(health, 1, (10, 10, 10))
            textpos = text.get_rect(
                center=((x + 0.5) * tile_width, (y + 0.5) * tile_height)
            )
            screen.blit(text, textpos)
              
        # Display the bombs
        for (x, y) in self.bombs:
            bomb_img = pygame.image.load(bomb_path).convert_alpha()
            bomb_img = pygame.transform.scale(bomb_img, (0.5*tile_width, 0.5*tile_height))
            screen.blit(bomb_img, ((x + 0.25) *tile_width, (y + 0.25)*tile_height))
            
        # Display the explosions
        for (x, y, _) in self.explosions:
            explosion_img = pygame.image.load(explosion_path).convert_alpha()
            explosion_img = pygame.transform.scale(explosion_img, (0.5*tile_width, 0.5*tile_height))
            screen.blit(explosion_img, ((x + 0.25) *tile_width, (y + 0.25)*tile_height))
            
        # Draw horizontal lines between tiles     
        for i in range(1, self.n):
            pygame.draw.line(
                screen,
                line_color,
                (0, tile_height * i),
                (self.width, tile_height * i),
                width=5,
            )
            
        # Draw vertical lines between tiles   
        for i in range(1, self.m):
            pygame.draw.line(
                screen,
                line_color,
                (tile_width * i, 0),
                (tile_width * i, self.height),
                width=5,
            )
            
        if (self.winner != None):
            if (self.winner == "None"):
                text_win = "Tie, nobody has won"
            else:
                text_win = F"Player {self.winner} has won"
            text = font.render(text_win, 1, (10, 10, 10), (125, 125, 125))
            textpos = text.get_rect(
                center=(self.width/2, self.height/2)
            )
            screen.blit(text, textpos)
            
    def transition(self):
        if (not self.ended()):
            return self
        print("Ended")
        self.menu.reset()
        return self.menu
