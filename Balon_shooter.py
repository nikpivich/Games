# подключение библиотек
# File -> Settings -> Project:<Название проекта> -> Python interpreter -> Клик на "+" ->
# -> В строке поиска "pygame" -> Нажать на "Install package" -> Дождаться зеленой строки "Package pygame installed succsesfully"
import pygame as pg
import random
from math import *


# Класс шарика. Отвечает за поведение шарика
# и отрисовку шарика
class Baloon:
    def __init__(self, speed): # Инициализация класса. Определение переменных
        # размер
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        # местоположение
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lower_bound
        # движение
        self.angle = 90
        self.speed = -speed
        self.probs = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        # длина нитки и цвет шарика
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])

    def show(self): # отрисовка
        # ниточка
        pg.draw.line(win, d_blue, (self.x + self.a / 2, self.y + self.b),
                     (self.x + self.a / 2, self.y + self.b + self.length))
        # основной шар
        pg.draw.ellipse(win, self.color, (self.x, self.y, self.a, self.b))

        # завязка
        pg.draw.ellipse(win, self.color, (self.x + self.a / 2 - 5,
                                          self.y + self.b - 3, 10, 10))
    # движение
    def move(self):
        # выбор направления движения
        direct = random.choice(self.probs)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10
        # двигаем шар
        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        # проверяем, что шар не вылетел за пределы экрана
        # если да - пытаемся вернуть его на экран
        if self.x + self.a > width or self.x < 0:
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y > height + 30:
            self.reset()
    # сброс местоположения шарика
    def reset(self):
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lower_bound
        self.angle = 90
        self.speed -= 0.002
    # проверяем не попал ли игрок в шарик
    def burst(self):
        global score
        pos = pg.mouse.get_pos()
        # получили местоположение мыши и если на шарике - то попал
        if on_baloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            return True
        else:
            return False

    # проверяем не вылетел ли шар наверх
    def get_out(self):
        if self.y < -self.b:
            return True
        else:
            return False


# инициализация pygame
pg.init()
# размер экрана
width = 500
height = 500
# настройа экрана
# создание экрана и установка названия окна
win = pg.display.set_mode((width, height))
pg.display.set_caption("Baloon shooter")
# запуск игровых часов
clock = pg.time.Clock()
# скрываем указатель мыши
pg.mouse.set_visible(False)
# параметры для игры
# отступ, размер нижней границы, счет, здоровье
margin = 100
lower_bound = 100
score = 0
health = 50
# цвета в игре
white = (230, 230, 230)
l_blue = (174, 214, 241)
red = (231, 76, 60)
l_green = (25, 111, 61)
d_gray = (40, 55, 71)
d_blue = (21, 67, 96)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
# шрифт
font = pg.font.SysFont("Ubuntu", 25)
# массив шариков
# создание и заполнение
# при создании с разной вероятностью выбираем скорость шарика
baloons = []
for index in range(10):
    baloons.append(Baloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4])))


# функция проверки нахождения курсора на шарике
# если координаты мыши находятся внутри прямоугольника
# с шариком, то возвращаем True, иначе False
def on_baloon(x, y, a, b, pos):
    if x < pos[0] < x + a and y < pos[1] < y + b:
        return True
    else:
        return False


# графика
def graph():
    # заливка
    win.fill(l_blue)
    # курсор
    pos = pg.mouse.get_pos()
    r = 25
    l = 20
    color = l_green
    # если курсор находить на шарике - меняем цвет
    for i in baloons:
        i.show()
        if on_baloon(i.x, i.y, i.a, i.b, pos):
            color = red
    # рисуем курсор
    # сначала основной круг, затем четыре черточки
    pg.draw.ellipse(win, color, (pos[0] - r /2, pos[1] - r / 2, r, r), 4)
    pg.draw.line(win, color, (pos[0], pos[1] - l / 2), (pos[0], pos[1] - l), 4)
    pg.draw.line(win, color, (pos[0] + l /2, pos[1]), (pos[0] + l, pos[1]), 4)
    pg.draw.line(win, color, (pos[0], pos[1] + l / 2), (pos[0], pos[1] + l), 4)
    pg.draw.line(win, color, (pos[0] - l / 2, pos[1]), (pos[0] - l, pos[1]), 4)
    # информационная панель снизу
    # прямоугольник + текст
    # сюда еще надо добавить счет
    pg.draw.rect(win, d_gray, (0, height - lower_bound, width, lower_bound))
    score_text = font.render("Baloons bursted: " + str(score), True, white)
    win.blit(score_text, (150, height - lower_bound + 50))
    health_text = font.render("Health: " + str(health), True, white)
    win.blit(health_text, (150, height - lower_bound + 10))
    pg.display.update()


# Экран конца игры
# заполняем
# пишем счет
def splash():
    win.fill(l_blue)
    txt = font.render("Game over", True, [0, 0, 0])
    win.blit(txt, (width / 2 - 50, height / 2))
    txt = font.render("Score: " + str(score), True, [0, 0, 0])
    win.blit(txt, (width / 2 - 50, height / 2 + 40))
    txt = font.render("Press any key to exit", True, [0, 0, 0])
    win.blit(txt, (width / 2 - 50, height / 2 + 80))
    pg.display.update()


# основной игровой цикл
run = True
game = True

while run:
    clock.tick(60)
    # рисуем графику
    if game:
        graph()
    # перебираем массив шариков
    # двигаем
    # Если вылетел за пределы экрана - отнимаем жизнь и удалаяем шар
    for item in baloons:
        item.move()
        if item.get_out():
            health -= 1
            baloons.pop(baloons.index(item))
    # если здоровье кончилось - конец игры
    # тут - просто остановка
    if health < 1:
        splash()
        game = False
        # run = False
    # стандартный перебор событий pygame для корректной работы программы
    # получаем все события - если было событие выхода - то останавливаем
    # основной игровой цикл и, соотвественно, выходим из игры
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # если была нажата ЛКМ
        if not game and event.type == pg.KEYDOWN:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            # перебираем шарики и смотри есть ли попадание
            # если да - то удаляем шар
            for item in baloons:
                if item.burst():
                    baloons.pop(baloons.index(item))
    # если количество шариков меньше, чем 9 + счет деленный на десять, то добавляем шарик
    if len(baloons) < 9 + score / 10:
        baloons.append(Baloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4])))

# корректный выход из приложения
pg.quit()