class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за доску"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Клетка уже выбрана"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Game_board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size

        self.count = 0

        self.fieled = [["O"]*size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res +="  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.fieled):
            res += f"\n{i+1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0<= d.x < self.size) and (0<= d.y < self.size))