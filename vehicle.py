from typing import List, Tuple

class Vehicle:
    def __init__(self, o, r, c, l, color):
        self.o, self.r, self.c, self.l, self.color = o, r, c, l, color

    # ---------------------------------------------------------------- util
    def cells(self):
        """Cases occupées (liste de couples ligne/colonne)."""
        return [
            (self.r + i, self.c) if self.o == "V" else (self.r, self.c + i)
            for i in range(self.l)
        ]

    def move(self, d, s=1):
        if d == "up":
            self.r -= s
        elif d == "down":
            self.r += s
        elif d == "left":
            self.c -= s
        elif d == "right":
            self.c += s

    def key(self):
        return self.o, self.r, self.c