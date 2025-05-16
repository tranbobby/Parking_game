from pathlib import Path
class Scores:
    FILE = Path("scores.txt")

    @classmethod
    def load(cls):
        if not cls.FILE.exists():
            return []
        out = []
        for line in cls.FILE.read_text("utf-8").splitlines():
            try:
                n, m, s, z = line.split(";")
                out.append((n, int(m), int(s), int(z)))
            except ValueError:
                pass
        return sorted(out, key=lambda x: (x[3], x[1], x[2]))

    @classmethod
    def save(cls, name, moves, sec, size):
        with cls.FILE.open("a", encoding="utf-8") as f:
            f.write(f"{name};{moves};{sec};{size}\n")