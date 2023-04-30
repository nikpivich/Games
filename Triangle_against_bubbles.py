# 1 ----------------- создание главного окна программы -------------------
from tkinter import *
HEIGHT = 500
WIDTH = 800
window = Tk()
window.title('Bubble Shooter')
c = Canvas(window, height=HEIGHT, width=WIDTH, bg='navyblue')
c.pack()

# 2 ---------------------- рисуем подлодку -----------------------------
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='yellow')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='pink')
SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)

# 3 ----------------------------- управление подлодкой ----------------------
SHIP_SPD = 30 # скорость подлодки
def move_ship (event):
   key = event.keysym
   if key == "Up":
       c.move(ship_id, 0, -SHIP_SPD)
       c.move(ship_id2, 0, -SHIP_SPD)
   elif key == "Down":
       c.move(ship_id, 0, SHIP_SPD)
       c.move(ship_id2, 0, SHIP_SPD)
   elif key == "Left":
       c.move(ship_id, -SHIP_SPD, 0)
       c.move(ship_id2, -SHIP_SPD, 0)
   elif key == "Right":
       c.move(ship_id, SHIP_SPD, 0)
       c.move(ship_id2, SHIP_SPD, 0)

c.bind_all('<Key>', move_ship) # при нажатии любой клавиши вызывается функция move_ship

# 4  -------------------------- пузыри разного размера и скорости --------------------------------
from random import randint
bub_id = list()                             # пустые списки для хранения имени, радиуса и скорости каждого пузыря
bub_r = list()
bub_speed = list()
MIN_BUB_R = 10                              # min и max радиус пузыря
MAX_BUB_R = 30
MAX_BUB_SPD = 10                            # max  скорость пузыря
GAP = 100                                   # смещение пузыря от края окна, чтобы он появлялся не сразу

def create_bubble():
   x = WIDTH + GAP                         # задает позицию пузыря на окне и его случайный радиус
   y = randint(0, HEIGHT)
   r = randint(MIN_BUB_R, MAX_BUB_R)
   id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='purple')   # рисуем пузырь
   bub_id.append(id1)                      # добавляет в списки имя, радиус и скорость пузыря
   bub_r.append(r)
   bub_speed.append(randint(1, MAX_BUB_SPD))

# 5 ------------------ # движение пузырей по экрану -------------------------
def move_bubbles():                         # функция перебирает все пузыри и двигает их
   for i in range(len(bub_id)):
       c.move(bub_id[i], -bub_speed[i], 0) # смещение пузыря по Х, по Y координата не меняеться

# 7 ---------------------------- по имени пузыря определяем, где он находится ---------------------
def get_coords(id_num):
   pos = c.coords(id_num)
   x = (pos[0] + pos[2])/2                 # вычисляет середину пузыря по Х
   y = (pos[1] + pos[3])/2                 # вычисляет середину пузыря по Y
   return x, y

# 8  ------------------------- удаляет пузыри ------------------------
def del_bubble(i):
   del bub_r[i]                            # удаляет пузырь из списка радиусов
   del bub_speed[i]                        # удаляет пузырь из списка скоростей
   c.delete(bub_id[i])                     # удаляет пузырь с холста
   del bub_id[i]                           # удаляет пузырь из списка имен

# 9 -------------------------------- удаляет пузыри, уплывшие за край холста -------------------------
def clean_up_bubs():
   for i in range(len(bub_id)-1, -1, -1):  # обратный цикл по списку пузырей - избежать ошибку работы FOR при удалении пузырей
       x, y = get_coords(bub_id[i])        # находит координаты пузыря
       if x < -GAP:                        # пузырь уплыл за край
           del_bubble(i)                   # удаляем пузырь, чтобы не замедлял игру

# 11 --------------------------  вычисляет расстояние между двумя объектами ------------------------
from math import sqrt                       # загружает функцию SQRT из модуля MATH
def distance(id1, id2):
   x1, y1 = get_coords(id1)                # координаты первого объекта
   x2, y2 = get_coords(id2)                # координаты вторового объекта
   return sqrt((x2 - x1)**2 + (y2 - y1)**2)# возвращает расстояние между объектами

# 12 ------------------------------ пузыри лопаются (большие и быстрые - больше очков) --------------------------
def collision():
   points = 0                              # переменная хранит набранные очки
   for bub in range(len(bub_id)-1, -1, -1):    # цикл проходит по всем пузырям из списка от последнего к 1, чтобы избежать ошибок при удалении
       if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]): # проверка: столкнулись ли подлодка и пузырь
           points += (bub_r[bub] + bub_speed[bub])                 # считает сколько очков дает пузырь и добавляет их к  POINTS
           del_bubble(bub)                                         # удаляет пузырь
   return points                           # возвращает количество набранных очков

# 14  ------------------------------ показывает счет и оставшееся время игры -------------------
c.create_text(50, 30, text='TIME', fill='red')                      # подпись времени
c.create_text(150, 30, text='SCORE', fill='red')                    # подпись очков
time_text = c.create_text(50, 50, text='TIME', fill='red')        # создает надпись для оставшегоя время
score_text = c.create_text(150, 50, text='SCORE', fill='red')     # создает надпись для очков
def show_score(score):
   c.itemconfig(score_text, text=str(score))                       # счет
def show_time(time_left):
   c.itemconfig(time_text, text=str(time_left))                    # оставшееся время


# 6 \ 10 \ 13 \ 15 \ 16                     главный цикл игры
from time import sleep, time
BUB_CHANCE = 10                             # частота появления пузырей
TIME_LIMIT = 30                             # время игры 30 секунд
BONUS_SCORE = 1000                          # за выигрыш в 1000 очков дается дополнительное время
score = 0                                   # очки в начале = 0
bonus = 0
end = time() + TIME_LIMIT                   # сохраняет время окончания игры
# MAIN GAME LOOP
while time() < end:                         # посторяет главный цикл до окончания времени
   if randint(1, BUB_CHANCE) == 1:         # случайное число от 1 до 10 (частота пузырей)
       create_bubble()                     # если число = 1 (это случай 1 из 10 возможных) - создается пузырь
   move_bubbles()                          # движение пузырей
   clean_up_bubs()                         # удаляем пузыри за экраном
   score += collision()                    # прибавляет очки за пузырь к счету
   if (int(score / BONUS_SCORE)) > bonus:  # вычисляет, когда добавить призовое время
       bonus += 1
       end += TIME_LIMIT
   show_score(score)                       # печатает счет в главном окне, а не консоли
   show_time(int(end - time()))            # показывает оставшееся время
   # print(score)                          # печатает счет в окне консоли
   window.update()                         # обновляет окно
   sleep(0.01)                             # замедление игры

# 17                                        GAME OVER
while True:
   window.update()
   c.create_text(MID_X, MID_Y, text='GAME OVER', fill='red', font=('Helvetica', 30))
   c.create_text(MID_X, MID_Y + 30, text='Score: ' + str(score), fill='red', font=15)
   c.create_text(MID_X, MID_Y + 60,text='Bonus time: '+ str(bonus*TIME_LIMIT), fill='red', font=15)

