import random
import heapq
from car import Car
from truck import Truck
class Board:
    COLORS = [
        "#F3722C",  # orange
        "#F9C74F",  # jaune
        "#90BE6D",  # vert clair
        "#43AA8B",  # vert
        "#577590",  # bleu gris
        "#277DA1",  # bleu
        "#9B5DE5",  # violet
    ]

    DIRS = ("up", "down", "left", "right")

    def __init__(self, size=6):
        self.size = size
        self.exit_row = size // 2
        self.v = []  # les véhicules


    def state(self):
        return tuple(v.key() for v in self.v)

    def set_state(self, st):
        for v, (o, r, c) in zip(self.v, st):
            v.o, v.r, v.c = o, r, c

    #le but
    def solved(self):
        red = self.v[0]
        return red.r == self.exit_row and red.c + red.l - 1 == self.size - 1

    #déplacement
    def can_move(self, idx, d):
        v = self.v[idx]

        if (v.o == "H" and d not in ("left", "right")) or (
            v.o == "V" and d not in ("up", "down")
        ):
            return False

        dr = -1 if d == "up" else 1 if d == "down" else 0
        dc = -1 if d == "left" else 1 if d == "right" else 0

        for r, c in v.cells():
            nr, nc = r + dr, c + dc

            #limite du plateau
            if not (0 <= nr < self.size and 0 <= nc < self.size):
                if idx == 0 and d == "right" and nr == self.exit_row and nc == self.size:
                    continue
                return False

            #gestion collision
            for j, u in enumerate(self.v):
                if j != idx and (nr, nc) in u.cells():
                    return False
        return True

    def move(self, idx, d):
        self.v[idx].move(d)

    def moves(self):
        for i in range(len(self.v)):
            for d in Board.DIRS:
                if self.can_move(i, d):
                    yield i, d

    def _h(self):
        red = self.v[0]
        dist = self.size - (red.c + red.l)
        blocks = sum(
            1
            for u in self.v[1:]
            if u.o == "V"
            and any(r == red.r for r, _ in u.cells())
            and u.c > red.c
        )
        return dist + 2 * blocks

    def solve(self, cap=150_000):
        start = self.state()
        pq = [(self._h(), 0, start, [])]
        best = {start: 0}

        while pq and cap:
            f, g, st, path = heapq.heappop(pq)
            cap -= 1
            self.set_state(st)

            if self.solved():
                self.set_state(start)
                return path

            for i, d in self.moves():
                self.move(i, d)
                nxt = self.state()
                self.move(i, {"up": "down", "down": "up", "left": "right", "right": "left"}[d])

                ng = g + 1
                if ng < best.get(nxt, 10**9):
                    best[nxt] = ng
                    heapq.heappush(pq, (ng + self._h(), ng, nxt, path + [(i, d)]))

        self.set_state(start)
        return None

    def preset(self, idx):
        self.v.clear()
        if idx == 1:
            self.size, self.exit_row = 6, 2
            self.v = [
                Car("H", 2, 0, "red"),
                Truck("V", 0, 3),
                Car("V", 0, 5),
                Truck("H", 4, 1),
                Car("H", 5, 3),
                Truck("V", 3, 5),
            ]
        elif idx == 2:
            self.size, self.exit_row = 8, 4
            self.v = [
                Car("H", 4, 0, "red"),
                Truck("V", 2, 2),
                Car("V", 0, 4),
                Truck("H", 6, 1),
                Car("H", 3, 5),
                Truck("V", 1, 7),
                Car("H", 7, 3),
            ]
        elif idx == 3:
            self.size, self.exit_row = 8, 3
            self.v = [
                Car("H", 3, 0, "red"),
                Truck("V", 0, 2),
                Car("H", 1, 4),
                Truck("H", 6, 1),
                Car("V", 2, 6),
                Truck("V", 4, 7),
                Car("H", 7, 3),
            ]

    def random_board(self):
        """Génère un plateau aléatoire SÛR : aucun chevauchement, pas
        déjà gagné, et toujours SOLVABLE."""
        while True:   
            #la voiture rouge spawn a la sortie donc on modifie ça
            start_c = random.randint(0, self.size - 3)
            self.v = [Car("H", self.exit_row, start_c, "red")]

            nb_slots = (self.size ** 2) // 6
            for _ in range(nb_slots):
                cls = Car if random.random() < 0.6 else Truck
                ori = random.choice(("H", "V"))
                length = 2 if cls is Car else 3
                max_row = self.size - (length if ori == "V" else 1)
                max_col = self.size - (length if ori == "H" else 1)

                for _ in range(300):
                    r = random.randint(0, max_row)
                    c = random.randint(0, max_col)
                    veh = cls(ori, r, c, random.choice(Board.COLORS))
                    if all(p not in u.cells() for u in self.v for p in veh.cells()):
                        self.v.append(veh)
                        break

            for _ in range(300):
                pm = [
                    (i, d) for i, d in self.moves()
                    if not (i == 0 and d == "right")
                ]
                if not pm:
                    break
                i, d = random.choice(pm)
                self.move(i, d)

            if self.solved():
                continue                     
            if self.solve():                  
                return                        
            
