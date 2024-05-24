from enum import Enum
import channel_client
import pygame

line_color = (0, 0, 0)


class Tile(Enum):
    O = "o"
    X = "x"
    EMPTY = ""


def tile_from_string(str):
    if str == "o":
        return Tile.O
    if str == "x":
        return Tile.X
    return Tile.EMPTY


class TicTacToeNetwork:
    def __init__(self, game, room_id):
        self.tictactoe = game
        self.socket = channel_client.connect_socket(
            "ws://localhost:4000/tictactoe/websocket?vsn=2.0.0"
        )
        self.lobby = f"room:{room_id}"
        channel_client.join_lobby(self.socket, self.lobby)

    def play(self, i, j, char):
        channel_client.send_message(
            self.socket, self.lobby, "play", {"i": i, "j": j, "c": char}
        )

    def check_play(self):
        message = channel_client.get_message(self.socket)
        if message is not None:
            type, payload = message[3], message[4]
            if type == "update":
                board = payload["board"]
                winner = payload["winner"]
                for i in range(3):
                    for j in range(3):
                        board[i][j] = tile_from_string(board[i][j])
                self.tictactoe.board = board
                if winner != "none":
                    self.tictactoe.player_won = tile_from_string(winner)

    def disconnect(self):
        channel_client.disconnect_socket(self.socket)


class TicTacToe:
    def __init__(self, player_id, width, height, room_id):
        self.board = [[Tile.EMPTY for _ in range(3)] for _ in range(3)]
        self.player_won = None
        self.network = TicTacToeNetwork(self, room_id)
        self.player_id = player_id
        self.width = width
        self.height = height

    def quit(self):
        self.network.disconnect()

    def play(self, pos):
        tile_width = self.width / 3
        tile_height = self.height / 3
        (x, y) = pos
        i = int(y // tile_height)
        j = int(x // tile_width)

        self.network.play(i, j, self.player_id.value)

    def update(self):
        self.network.check_play()

    def display(self, screen):
        tile_width = self.width / 3
        tile_height = self.height / 3
        for i in range(1, 3):
            pygame.draw.line(
                screen,
                line_color,
                (0, tile_height * i),
                (self.width, tile_height * i),
                width=5,
            )
        for i in range(1, 3):
            pygame.draw.line(
                screen,
                line_color,
                (tile_width * i, 0),
                (tile_width * i, self.height),
                width=5,
            )

        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        for i in range(3):
            for j in range(3):
                char = self.board[i][j].value
                text = font.render(char, 1, (10, 10, 10))
                textpos = text.get_rect(
                    center=((j + 0.5) * tile_width, (i + 0.5) * tile_height)
                )
                screen.blit(text, textpos)

        # if won
        if self.player_won is not None:
            font = pygame.font.Font(pygame.font.get_default_font(), 36)
            text = font.render(
                f"Player {self.player_won.value} has won", 1, (10, 10, 10)
            )
            temp_surface = pygame.Surface(text.get_size())
            temp_surface.fill((192, 192, 192))
            textpos = text.get_rect(center=(self.width / 2, self.height / 3))
            temp_surface.blit(text, (0, 0))
            screen.blit(temp_surface, textpos)
