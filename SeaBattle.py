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
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.count = 0

        self.fieled = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.fieled):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=True):
        """
        Метод contour заполняет пространство вокруг коробля на одну клетку.
        Список near содержит все элементы вокруг центральной точки
        В цилке проходим по точкам коробля и передаем d значение вида Dot(1, 2)
        Во вложенном цикле проходим по списку near, и присваиваем dx и dy значения элементов списка. Далее в значение
        cur записываем значение точки у корабля.
        :param ship: вызываем Ship: Ship(Dot(1, 2), 4, 0)
        :param verb: видимость поля вокруг кораблей.
        :return:
        """
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.fieled[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        """
        Метод добавления корабля на поле. В первом цикле проходим по всем точкам корабля, проверяем не занята ли
        координата корабля, если введенная координата занята то выводим ошибку.
        Во втором цикле присваиваем меняем значение точек коробля на квадрат.
        :param ship:
        :return:
        """
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.fieled[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)
    def shot(self, d):
        """
        Метод Shot.
        Проверяем выходит ли точка за границы поля.
        Проверяем не занята ли точка.
        Если проверки пройдены, то добавляем точку в список занятых.
        В цикле из точек корабля проходим по кораблям, и проверяем принадлежность точки к ним. Если точка есть в корабле,
        то убираем у lives единицу. Меняем значение в поле на Х. Проходим проверку, если жизни равны нулю то увеличиваем
        счетчик count на 1, делаем контур видимым и выводим сообщение Корабль уничтожен. Иначе корабль ранен.
        Если точки нет в списке кораблей то меняем значение поля на точку и выводим сообщение мимо
        :param d:
        :return:
        """
        if self.out(d):
            raise BoardOutException

        if d in self.busy:
            raise BoardUsedException

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.fieled[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.fieled[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []
