from random import randint


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
    """
    C помощью этого класса будем задавать точки с двумя координатами в виде строки "Dot(x, y)" .
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        __eq__ используется для сравнения значений атрибутов класса
        Форма записи    a = Dot(1, 1)
                        b = Dot(1, 1)
                        print(a.x == b.x and a.y == b.y)
        Будет равна    print(a == b)
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """
        __repr__ используется для возможности вывода текстовой информации print(a)
        :return: # Dot(1, 1)
        """
        return f"Dot({self.x}, {self.y})"


class Ship:
    """
        Класс Ship в нем задаем параметры корабля: начальную точку с помощью класса Dot, длину и направление постановки
    корабля.
    В методе dots создаем пустой массив, в цикле проходим по длине корабля, создаем значение начальной точки, и в каждой
    точке длинны увеличиваем координату в зависимости от направления на значение длинны в этой точки
    Получаем список вида [Dot(1, 1), Dot(2, 1), Dot(3, 1), Dot(4, 1), Dot(5, 1)]
    """
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        """
        Метод с декоратором позволяет обращаться к нему без вызова.
        Создаем пустой массив ship_dots в который будем помещать точки объекта.
        Цикл от 0 до длинны -1 в котором мы определяем координаты точки коробля.
        Если направление 0, то корабль расположен горизонтально и мы увеличиваем x координату на значение i.
        Если направление 1, то корабль расположен вертикально и мы увеличиваем y координату на значение i.
        В конце добавляем к массиву значение координат точки.
        :return: [Dot(1, 2), Dot(2, 2), Dot(3, 2), Dot(4, 2)]
        """
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
        """
        Метод провеки выстрелов, возвращает True если shot есть в списке dots
        :param shot: Dot(1, 2)
        :return: True
        """
        return shot in self.dots


class Game_board:
    """
    Класс Game_board отрисовывает игровое поле.
    """
    def __init__(self, hid=False, size=6):
        """
        В атрибут fieled создаем список из списков нулей равных размеру поля
        имеет вид [['O', 'O', 'O', 'O', 'O', 'O'], ... , ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']
        :param hid: видимость поля
        :param size: размер поля
        """
        self.hid = hid
        self.size = size

        self.count = 0

        self.fieled = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        """
            Метод def __str__ позволяет нам выводить поле без вызова функции, а именно:
        board = Game_board()
        print(board)
        В этом методе мы проходим в цикле с помощью функции enumerate по элементам списка, при этом i присваивается
        значение индекса, а row значение самого элемента.
        :return:
        """
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.fieled):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        """
         Метод out контролирует что введенные значения в пределах поля.
        :param d: Вызов Dot и передача значений координат точки.
        :return: True если координаты точки выходят за пределы поля
        """
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
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
        В цикле из точек корабля проходим по кораблям, и проверяем принадлежность точки к ним. Если точка есть в
        корабле, то убираем у lives единицу. Меняем значение в поле на Х. Проходим проверку, если жизни равны нулю то
        увеличиваем счетчик count на 1, делаем контур видимым и выводим сообщение Корабль уничтожен. Иначе корабль ранен
        Если точки нет в списке кораблей, то меняем значение поля на точку и выводим сообщение мимо
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


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        """
        Ход компьютера
        Вызываем класс Dot и присваиваем значениям координат рандомные числа от 0 до 5.
        :return: Dot(randint(0, 5), randint(0, 5))
        """
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        """
        Ход игрока.
        В цикле ввод игроком двух чисел.
        Проходим проверку, игрок должен ввести два числа. Если проверка пройдена, то присваиваем x и y значения
        нулевого и первого индекса списка.
        Проходим проверку содержат ли троки x и y числа, если да то интуем значения x и y.
        Возвращаем вызов класса Dot с передачей координат.
        :return: Dot(x - 1, y - 1)
        """
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        """
        Указываем размер поля.
        Генерируем две доски для компьютера и игрока.
        Скрываем поле компьютера.
        И создаем два атрибута игрока и компьютера и передаем им значения поля.
        :param size:
        """
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def try_board(self):
        """
        Расстановка кораблей. Указываем список lens в который передаем размерность кораблей.
        Атрибут attempts количество попыток расстановки кораблей на поле.
        :return:
        """
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Game_board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 10000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def loop(self):
        """
        num - номер хода.

        :return:
        """
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
print(g.start())
