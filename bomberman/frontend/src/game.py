import pygame
import sys
from pygame.locals import *
from menu import Menu
import argparse

pygame.init()

# Colours
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bomberman")

player_id = "P1"
#host="localhost:4000"
host="10.109.134.223:4000"

# The main function that controls the game
def main():
    state = Menu(WINDOW_WIDTH, WINDOW_HEIGHT, host)
    # The main game loop
    while True:
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                state.quit()
                pygame.quit()
                sys.exit()
            state.event(event)
                
        # Processing
        # This section will be built out later
        state.update()

        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        state.display(WINDOW)
        pygame.display.update()
        fpsClock.tick(FPS)
        state = state.transition()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost:4000", help="Host running the room server")
    args = parser.parse_args()
    host = args.host
    main()
