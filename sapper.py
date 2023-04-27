import tkinter
import random
import tkinter.simpledialog
import tkinter.messagebox
# создаем окно
win = tkinter.Tk()
win.title("Sapper")
# переменные для игры
gameover = False
rows = 10
cols = 10
mines = 10
field = []
buttons = []
customsizes = []
colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
first_step = True


# создание верхней панели меню
def create_menu():
    # панель
    menubar = tkinter.Menu(win)
    # раздел Размер
    menusize = tkinter.Menu(win, tearoff=0)
    menusize.add_command(label="small (10x10) with 10 mines", command=lambda: set_size(10, 10, 10))
    menusize.add_command(label="medium (20x20) with 40 mines", command=lambda: set_size(20, 20, 40))
    menusize.add_command(label="big (35x35) with 120 mines", command=lambda: set_size(35, 35, 120))
    menusize.add_command(label="custom", command=custom_size)
    menusize.add_separator()
    # если были выбраны пользовательские конфигурации поля, то отображаем их
    for i in range(0, len(customsizes)):
        menusize.add_command(label=str(customsizes[i][0]) + "x" + str(customsizes[i][1]) + " with " +
                             str(customsizes[i][2]) + " mines", command=lambda csz = customsizes:
                             set_size(csz[i][0], csz[i][1], csz[i][2]))
    # собираем меню
    menubar.add_cascade(label="Size", menu=menusize)
    # вешаем выход на пункт выхода
    menubar.add_cascade(label="Exit", command=lambda: win.destroy())
    win.config(menu=menubar)


# создаем поле на экране из кнопок
def create_field():
    global rows, cols, buttons
    # кнопка рестарт
    tkinter.Button(win, text="Restart", command=restart_game).grid(row=0, column=0, columnspan=cols,
                                                                   sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    # само поле
    # все кнопки хранятся в одном массиве
    buttons = []
    # создаем кнопки
    for i in range(0, rows):
        buttons.append([])
        for j in range(0, cols):
            # сама кнопка, плюс лямбда функция, чтобы вызвать функцию и передать в нее параметры - местоположение кнопки
            btn = tkinter.Button(win, text=" ", width=2, command=lambda x=i, y=j: btn_click(x, y))
            # цепляем правый клик мыши
            btn.bind('<Button-3>', lambda e, x=i, y=j: mouse_click(x, y))
            # размещаем кнопку
            btn.grid(row=i+1, column=j, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            # добавляем в массив
            buttons[i].append(btn)


# обработка нажатия на кнопку
def btn_click(x, y):
    global cols, rows, field, buttons, colors, gameover, first_step
    # ничего не делаем, если игра закончилась
    if gameover:
        return
    # если это первых ход, то проверяем есть ли тут бомба
    # если есть - то заполняем поле бомбами заново, пока не будет пустой ячейки
    if first_step:
        while field[x][y] == -1:
            create_field()
        first_step = False
    # если в ячейке бомба
    # кнопку делаем красной
    # отображаем остальные бомбы и подсвечиваем их желтым
    # сообщаем о проигрыше
    if field[x][y] == -1:
        gameover = True
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background="red", disabledforeground="black")
        tkinter.messagebox.showinfo("Game Over", "You have lost")
        for i in range(0, rows):
            for j in range(0, cols):
                if field[i][j] == -1 and i != x and j != y:
                    buttons[i][j]["text"] = "*"
                    buttons[i][j].config(background="yellow", disabledforeground="black")
    # если пустая ячейка
    # если рядом есть бомба отображаем цифру, если нет - открываем соседние пустые ячейки
    elif field[x][y] > 0:
        buttons[x][y]["text"] = str(field[x][y])
        buttons[x][y].config(disabledforeground=colors[field[x][y]])
    else:
        buttons[x][y]["text"] = " "
        auto_click(x, y);
    # отключаем кнопку и меняем ее форму
    buttons[x][y]["state"] = "disabled"
    buttons[x][y].config(relief=tkinter.SUNKEN)
    check_win()


# проверка на выигрыш
def check_win():
    global buttons, field, rows, cols
    win = True
    # елси есть хотя бы одна закрытая клетка, то победы нет, иначе - есть
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        tkinter.messagebox.showinfo("Game Over", "You have won!")


# проход поля для открытия соседних пустых ячеек

#
# ФУНКЦИЯ ВЫЗЫВАЕТСЯ РЕКУРСИВНО
#
def auto_click(x, y):
    global field, buttons, colors, rows, cols
    # если кнопка выключена - возвраь
    if buttons[x][y]["state"] == "disabled":
        return
    # если ячейка возле бомбы - отображаем количество бомб, иначе - ничего
    if field[x][y] > 0:
        buttons[x][y]["text"] = str(field[x][y])
    else:
        buttons[x][y]["text"] = " "
    # настраиваем кнопку
    buttons[x][y].config(disabledforeground=colors[field[x][y]])
    buttons[x][y]["state"] = "disabled"
    buttons[x][y].config(relief=tkinter.SUNKEN)
    # если ячейке не возле бомбы, то опрашиваем соседние ячейки
    # чтобы опросить необходимо проверить их существование
    # нумерация ячеек далее:
    # 123
    # 4x6
    # 789
    # где Х - текущая клетка
    # С - верхняя граница
    # Ю - нижняя граница
    # З - левая граница
    # В - правая граница

    if field[x][y] == 0:
        # если не у СЗ, то "кликаем" по 1
        if x != 0 and y != 0:
            auto_click(x-1, y -1)
        # если не у С, то 2
        if x != 0:
            auto_click(x - 1, y)
        # если не у СВ, то 3
        if x != 0 and y != cols - 1:
            auto_click(x - 1, y + 1)
        # если не у З, то 4
        if y != 0:
            auto_click(x, y - 1)
        # если не у В, то 6
        if y != cols - 1:
            auto_click(x, y + 1)
        # если не у ЮЗ, то 7
        if x != rows -1 and y != 0:
            auto_click(x + 1, y - 1)
        # если не у Ю, то 8
        if x != rows - 1:
            auto_click(x + 1, y)
        # если не у ЮВ, то 9
        if x != rows - 1 and y != cols - 1:
            auto_click(x + 1, y + 1)


# обработка правого клика мышки по кнопке
def mouse_click(x, y):
    global buttons
    # если конец игры - то ничего не делаем, возврат
    if gameover:
        return
    # если на кнопке стоит ? (флаг), то снимаем, иначе ставим
    if buttons[x][y]['text'] == "?":
        buttons[x][y]['text'] = " "
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]['text'] == " " and buttons[x][y]["state"] == "active":
        buttons[x][y]['text'] = "?"
        buttons[x][y]["state"] = "disabled"
        buttons[x][y].config(disabledforeground="#000000")


# установка размера поля
def set_size(r, c, m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    restart_game()


# рестарт
def restart_game():
    global gameover, first_step
    gameover = False
    first_step = True
    # удаляем с экрана все, кроме меню
    for item in win.winfo_children():
        if type(item) != tkinter.Menu:
            item.destroy()
    # создаем поле на экране и игру
    create_field()
    create_game()


# настройка собственных размеров игры
def custom_size():
    global customsizes
    # создаем три диалога, где справшиваем про количество рядов, колонок и мин
    r = tkinter.simpledialog.askinteger("Custom size", "Enter ammount of rows")
    c = tkinter.simpledialog.askinteger("Custom size", "Enter ammount of columns")
    m = tkinter.simpledialog.askinteger("Custom size", "Enter ammount of mines")
    # если мин больше, чем ячеек на поле минус одна
    # переспрашиваем про количество мин, пока их не будет РЯДЫ * КОЛОНКИ - 1
    while m > r * c:
        m = tkinter.simpledialog.askinteger("Custom sizes", "Maximum mines is: " + str(r * c) + "\nEnter ammount of mines")
    # сохраняем настройки
    customsizes.insert(0, (r, c, m))
    customsizes = customsizes[0:5]
    set_size(r, c, m)
    # пересоздаем меню
    create_menu()


# создаем игру, фактически - поле с минмами
def create_game():
    global rows, cols, mines, field
    field = []
    # создаем массив из 0 размером с поле
    for i in range(0, rows):
        field.append([])
        for j in range(0, cols):
            field[i].append(0)
    # заполняем его минами
    for i in range(0, mines):
        # получаем две случайные координаты
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        # если попали в занятую ячейку, то создаем заново, пока не будет пустая
        while field[x][y] == -1:
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)
        # записываем
        field[x][y] = -1
        # добавляем 1 к счетчикам вокруг мины
        # принцип, как и с опросом
        # проверяем на существование, если существует и там не бомба, то добавляем 1
        if x != 0:
            if y != 0:
                if field[x -1][y - 1] != -1:
                    field[x - 1][y - 1] += 1
            if field[x - 1][y] != -1:
                field[x - 1][y] += 1
            if y != cols - 1:
                if field[x - 1][y + 1] != -1:
                    field[x - 1][y + 1] += 1
        if y != 0:
            if field[x][y - 1] != -1:
                field[x][y - 1] += 1
        if y != cols - 1:
            if field[x][y + 1] != -1:
                field[x][y + 1] += 1
        if x != rows - 1:
            if y != 0:
                if field[x + 1][y - 1] != -1:
                    field[x + 1][y - 1] += 1
            if field[x + 1][y] != -1:
                field[x + 1][y] += 1
            if y != cols - 1:
                if field[x + 1][y + 1] != -1:
                    field[x + 1][y + 1] += 1


# запуск игры
# создаем последовательно, меню, поле кнопок и игровое поле
# вешаем экран
create_menu()
create_field()
create_game()
win.mainloop()