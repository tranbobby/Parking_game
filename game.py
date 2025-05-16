import tkinter as tk
import time
from tkinter import messagebox, simpledialog
from typing import Optional
from board import Board
from scores import Scores
class Game:
    CELL = 90  #tailel des cases en px

    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Jam Game")
        self.bg = self._load_bg()
        self.map_size = tk.IntVar(value=6)

        # frames
        self.menu = tk.Frame(root)
        self.opts = tk.Frame(root)
        self.scores_f = tk.Frame(root)
        self.play = tk.Frame(root)

        self._build_menu()
        self.menu.pack(fill="both", expand=True)

    def _load_bg(self):
        try:
            return tk.PhotoImage(file="menu_bg.png")
        except Exception:
            return None

    def _set_bg(self, frame):
        for w in frame.winfo_children():
            w.destroy()
        if self.bg:
            tk.Label(frame, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame.configure(bg="#222")

    #menu
    def _build_menu(self):
        self._set_bg(self.menu)
        tk.Label(
            self.menu,
            text="Traffic Jam Game",
            font=(None, 32, "bold"),
            fg="white",
            bg="#222",
        ).pack(pady=40)

        for txt, cmd in (
            ("Jouer", self.choose_map),
            ("Options", self.show_opts),
            ("Scores", self.show_scores),
            ("Quitter", self.root.quit),
        ):
            tk.Button(self.menu, text=txt, font=(None, 16), width=18, command=cmd).pack(
                pady=8
            )

    def back_menu(self):
        for f in (self.opts, self.scores_f, self.play):
            f.pack_forget()
        self.menu.pack(fill="both", expand=True)

    #options
    def show_opts(self):
        self.menu.pack_forget()
        self._set_bg(self.opts)
        self.opts.pack(fill="both", expand=True)

        tk.Label(
            self.opts,
            text="Taille du plateau :",
            font=(None, 16),
            fg="white",
            bg="#222",
        ).pack(pady=30)

        tk.OptionMenu(self.opts, self.map_size, 6, 8).pack()
        tk.Button(self.opts, text="Retour", font=(None, 14), command=self.back_menu).pack(
            pady=40
        )

    #score
    def show_scores(self):
        self.menu.pack_forget()
        self._set_bg(self.scores_f)
        self.scores_f.pack(fill="both", expand=True)

        tk.Label(
            self.scores_f,
            text="Scores",
            font=(None, 24, "bold"),
            fg="white",
            bg="#222",
        ).pack(pady=20)

        sc = Scores.load()
        if not sc:
            tk.Label(
                self.scores_f,
                text="Aucun score pour le moment.",
                fg="white",
                bg="#222",
            ).pack(pady=10)
        else:
            for i, (n, m, s, z) in enumerate(sc, 1):
                msg = f"#{i:02} – {n} : {m} coups, {s//60:02}:{s%60:02}  (taille {z})"
                tk.Label(
                    self.scores_f,
                    text=msg,
                    fg="white",
                    bg="#222",
                    anchor="center",
                    justify="center",
                ).pack(fill="x", padx=30, pady=2)

        tk.Button(
            self.scores_f, text="Retour", font=(None, 14), command=self.back_menu
        ).pack(pady=30)

    #choix de map
    def choose_map(self):
        self.menu.pack_forget()
        self._set_bg(self.opts)
        self.opts.pack(fill="both", expand=True)

        tk.Label(
            self.opts,
            text="Choisissez une carte :",
            font=(None, 18),
            fg="white",
            bg="#222",
        ).pack(pady=25)

        for i in (1, 2, 3):
            tk.Button(
                self.opts,
                text=f"Config {i}",
                font=(None, 14),
                width=16,
                command=lambda i=i: self.start_game(i),
            ).pack(pady=4)

        tk.Button(
            self.opts,
            text="Aléatoire",
            font=(None, 14),
            width=16,
            command=lambda: self.start_game(None),
        ).pack(pady=8)

        tk.Button(self.opts, text="Retour", font=(None, 14), command=self.back_menu).pack(
            pady=25
        )

    #start la game
    def start_game(self, preset: Optional[int]):
        self.board = Board(self.map_size.get())
        if preset:
            self.board.preset(preset)
        else:
            self.board.random_board()
        self.move_count = 0
        self.selected = None
        self.help_used = False
        self.start_t = time.time()

        #fps
        self.opts.pack_forget()
        self._set_bg(self.play)
        self.play.pack(fill="both", expand=True)
        self.play.grid_rowconfigure(0, weight=1)
        self.play.grid_columnconfigure(0, weight=1)

        w = self.CELL * (self.board.size + 1)
        h = self.CELL * self.board.size
        self.canvas = tk.Canvas(
            self.play, width=w, height=h, bg="white", highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.on_click)

        side = tk.Frame(self.play, bg="#222")
        side.grid(row=0, column=1, sticky="n", padx=20, pady=20)

        self.timer_lbl = tk.Label(
            side, text="Temps : 00:00", font=(None, 16), bg="#222", fg="white"
        )
        self.timer_lbl.pack(pady=(0, 20))

        self.solve_btn = tk.Button(
            side, text="Solution", font=(None, 14), command=self.on_solve
        )
        self.solve_btn.pack(pady=8)

        tk.Button(side, text="Menu", font=(None, 14), command=self.back_menu).pack(
            pady=8
        )

        for k in ("<Up>", "<Down>", "<Left>", "<Right>"):
            self.root.bind(k, self.on_key)

        self._tick()
        self.draw()

    #timer
    def _tick(self):
        elapsed = int(time.time() - self.start_t)
        self.timer_lbl.config(text=f"Temps : {elapsed//60:02}:{elapsed%60:02}")
        self.timer_id = self.root.after(1000, self._tick)

    #affiche le plateau
    def draw(self):
        b = self.board
        C = self.CELL
        self.canvas.delete("all")

        #quadrillage
        for i in range(b.size + 1):
            self.canvas.create_line(
                0, i * C, b.size * C, i * C, fill="#aaa", stipple="gray50"
            )
            self.canvas.create_line(
                i * C, 0, i * C, b.size * C, fill="#aaa", stipple="gray50"
            )

        #goal
        er = b.exit_row
        self.canvas.create_rectangle(
            b.size * C,
            er * C,
            (b.size + 1) * C,
            (er + 1) * C,
            fill="#7CFC00",
            outline="",
        )

        #vehicule
        for idx, v in enumerate(b.v):
            r1, c1 = v.cells()[0]
            r2, c2 = v.cells()[-1]
            self.canvas.create_rectangle(
                c1 * C,
                r1 * C,
                (c2 + 1) * C,
                (r2 + 1) * C,
                fill=v.color,
                outline="#FFFF00" if idx == self.selected else "#000",
                width=3,
            )

    def on_click(self, e):
        col, row = e.x // self.CELL, e.y // self.CELL

        # sélection
        for i, v in enumerate(self.board.v):
            if (row, col) in v.cells():
                self.selected = i
                self.draw()
                return

        if self.selected is None:
            return

        v = self.board.v[self.selected]
        d = None
        if v.o == "H" and row == v.r:
            d = "left" if col < v.c else "right" if col > v.c + v.l - 1 else None
        elif v.o == "V" and col == v.c:
            d = "up" if row < v.r else "down" if row > v.r + v.l - 1 else None

        if d and self.board.can_move(self.selected, d):
            self.board.move(self.selected, d)
            self.move_count += 1  
            self.draw()
            self.check_win()

    def on_key(self, e):
        if self.selected is None:
            return
        mp = {"Up": "up", "Down": "down", "Left": "left", "Right": "right"}
        d = mp.get(e.keysym)
        if d and self.board.can_move(self.selected, d):
            self.board.move(self.selected, d)
            self.move_count += 1 
            self.draw()
            self.check_win()

    #resoudre
    def on_solve(self):
        self.help_used = True
        self.solve_btn.config(state="disabled")

        sol = self.board.solve()
        if not sol:
            messagebox.showwarning("Erreur", "Pas de solution")
            return
        self.anim(sol)

    def anim(self, moves):
        if not moves:
            self.check_win()
            return
        i, d = moves.pop(0)
        self.board.move(i, d)
        self.draw()
        self.root.after(200, lambda: self.anim(moves))

    #cas victoire
    def check_win(self):
        if not self.board.solved():
            return
        self.root.after_cancel(self.timer_id)
        if self.help_used:
            messagebox.showinfo("Bravo", "Puzzle résolu (non classé)")
            self.back_menu()
            return
        elapsed = int(time.time() - self.start_t)
        moves = self.move_count
        name = simpledialog.askstring(
            "Gagné !", "Entrez votre nom pour enregistrer votre score :"
        )
        if name:
            Scores.save(name, moves, elapsed, self.board.size)
        self.back_menu()