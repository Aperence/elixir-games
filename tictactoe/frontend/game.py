import pygame
import sys
from pygame.locals import *
import argparse
from tictactoe import TicTacToe, Tile

parser = argparse.ArgumentParser()

parser.add_argument("player", type=str)
parser.add_argument("room_id", type=int)

args = parser.parse_args()

pygame.init()

# Colours
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# The main function that controls the game
def main():
    looping = True
    tile = None
    if args.player == "X":
        tile = Tile.X
    if args.player == "O":
        tile = Tile.O
    state = TicTacToe(tile, WINDOW_WIDTH, WINDOW_HEIGHT, args.room_id)

    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                state.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                state.play(pos)

        # Processing
        # This section will be built out later
        state.update()

        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        state.display(WINDOW)
        pygame.display.update()
        fpsClock.tick(FPS)


main()
