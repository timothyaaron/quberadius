import random
from collections import OrderedDict

import arcade

from constants import PLAYER_COLORS, WIDTH
from objects.power import Power


class Piece(arcade.Sprite):
    POWER_TEXTURE = arcade.load_texture(":resources:images/tiles/boxCrate_double.png")

    def __init__(self, player, **kwargs):
        super().__init__(
            center_x=0,
            center_y=0,
            image_width=128,
            image_height=128,
            scale=WIDTH / 128 / 1.4,
            filename=":resources:images/tiles/boxCrate.png",
            angle=random.randint(-5, 5),
        )
        self.alpha = 160
        self.player = player
        self.square = None
        self.powers = OrderedDict()
        self.turns = 0

        self.append_texture(Piece.POWER_TEXTURE)
        for _ in range(random.randint(0, 3)):
            self.add_power()

    def __repr__(self):
        return f"Player {self.player.idx})"

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
        self.color = PLAYER_COLORS[value.idx]

    def add_power(self, name=None):
        name = name or random.choice([
            "Destroy Row", "Destroy Column",
            "Lower Row", "Lower Column", "Lower",
        ])
        if name in self.powers:
            self.powers[name].count += 1
        else:
            self.powers[name] = Power(name)
        self.set_texture(1)

    def use_power(self, square):
        board = self.square.board
        debug_window = board.game.debug_window
        power = self.powers.get(board.power)
        if power.is_valid(square, board.game):
            if power.execute(square):
                debug_window.text = "Boom."
                square.piece.decrement_power(power.name)
            else:
                debug_window.text = "Not useful now. Deactivating."

        board.selected = None
        board.power = None

    def decrement_power(self, name, count=1):
        power = self.powers.get(name)

        if power:
            power.count -= count
            if power.count <= 0:
                del self.powers[power.name]

            if not self.powers:
                self.set_texture(0)

    def can_move_to(self, square):
        column = self.square.column
        row = self.square.row
        for i in range(column-1, column+2):
            for j in range(row-1, row+2):
                try:
                    if self.square.board.grid[i][j] == square:
                        return True
                except Exception:
                    pass
        return False
