import pygame

class Scene:
    def update(self):
        ...
    
    def display(self, screen : pygame.Surface):
        ...
    
    def transition(self):
        ...
        
    def event(self, event : pygame.event.Event) -> None:
        ...
        
    def quit() -> None:
        ...