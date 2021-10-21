import threading                    # для многопоточности
from tkinter.ttk import *           # для combobox
import random
from tkinter.filedialog import *    # для окна приложения и для TK()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time

# метка времни              !!ПЕРЕД ФУНКЦИЯМИ
time_sec = time.strftime('%H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_filename = time.strftime('%Y_%m_%d')        # год_месяц_день
time_year = time.strftime('%Y')    # год_месяц_день_час_минута_сек
time_sec = time.strftime('%S')    # год_месяц_день_час_минута_сек
print(time_sec)

# создание окна программы
root = Tk()
root.title('ПТИ')

# создание контенера для кнопок, комбобокса и т.д.
labelTop = LabelFrame(root, text='')
labelTop.grid(column=0, row=2)
# Label(labelTop, text='частота обновления, с').grid(column=1, row=2)

# создание контенера для графика ТЕМПЕРАТУРА
labelGrath_T = LabelFrame(root, text='')
labelGrath_T.grid(column=0, row=0)

# создание контенера для графика ВЛАЖНОСТЬ
labelGrath_H = LabelFrame(root, text='')
labelGrath_H.grid(column=0, row=1)

# # создание списка частоты записи
# spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
# menu_sec = Combobox(labelTop, values=spisok_t, width=2, height=11)
# menu_sec.grid(column=2, row=2)
# menu_sec.insert(0, spisok_t[0])     # по дефолту ставим 60 сек

# создание 1 графика ТЕМПЕРАТУРА
fig, ax, = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
line_T, = ax.plot([], [], color='blue', ls='solid', lw=1.5)          # линия для графика Температуры
ax.grid()
fig.set_size_inches(6.0, 2.0)
ax.set_title('Температура')                 # название графика
# ax.set_xlabel('время')                       # название оси X
xdata_T, ydata_T = [], []                   # массив данных для X и Y для 1 графика
ax.set_ylim(10, 40)  # лимиты по оси Y
# ax.set_xlim(int(time_year), 60)  # лимиты по оси Y в tuple сохряняет - работает
ax.set_xlim(int(time_sec), int(time_sec)+60)  # лимиты по оси Y в tuple сохряняет
print(type(ax.set_xlim()))
canvas = FigureCanvasTkAgg(fig, master=labelGrath_T)    # отрисовка графики в tkinter
                                                        # FigureCanvasTkAgg - искать в инете для
                                                        # решения двух графиков
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# # создание 2 графика ВЛАЖНОСТЬ
# fig1, ax1, = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
# line_H = ax1.plot([], [], color='blue', ls='solid', lw=1.5)
# ax1.grid()
# fig1.set_size_inches(6.0, 2.0)
# ax1.set_title('Влажность')                 # название графика
# ax1.set_xlabel('время')                       # название оси
# # ax1.set_ylabel('температура')
# x1data_H, y1data_H = [], []
# ax1.set_ylim(20, 80)  # лимиты по оси Y
# ax1.set_xlim(0, 60)  # лимиты по оси Y
# # отрисовка осей и подписей к 2 графику
# canvas1 = FigureCanvasTkAgg(fig1, master=labelGrath_H)
# canvas1.show()
# canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # положение окна с осями

# функция запуска ПТИ
pause = True
def start():
    data_temp = 25 + random.randint(-5, 5)
    data_vlag = 50 + random.randint(-10, 10)
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    # ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=1000,
    #                                repeat=False, init_func=init)
    # threading.Timer(int(menu_sec.get()), start).start()
    global pause
    # print(pause)
    pause ^= True
    # print(data)
    # print (pause)
    B1.configure(state=DISABLED)
    return (data_vlag, data_temp, ani)

# функция запуска ПТИ в сом порт
def start_com():
    # PTI_COM.open()
    data_temp = 25 + random.randint(-5, 5)
    data_vlag = 50 + random.randint(-10, 10)
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    # PTI_COM.write(data.encode('utf-8'))             # отправляем в COM порт
    # PTI_COM.close()
    threading.Timer(int(menu_sec.get()), start_com).start()

# функция закрытия приложения
def quit():
    # PTI_COM.close()
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# функция для начального состояния графика
def init():
    del xdata_T[:]                        # очистка массива исходных данных для X для 1 графика
    del ydata_T[:]                        # очистка массива исходных данных для Y для 1 графика
    # del xdata_2[:]                      # очистка массива исходных данных для X для 2 графика
    # del ydata_2[:]                      # очистка массива исходных данных для Y для 2 графика
    # line_T.set_data(xdata_T, ydata_T)         # в качестве данных для 1 графика будут xdata и ydata
    # line_2.set_data(xdata_2, ydata_2)     # в качестве данных для 1 графика будут xdata и ydata
    return line_T

# функция для обновления графика
def run(data):
    # print(data)
    # print(ani)
    # update the data
    # t, y, y_2 = data
    t, y, y_2 = data                          # связан с выходом функции data_gen  yield t, (cnt)
    xdata_T.append(t)
    ydata_T.append(y)
    # x1data_H.append(t)
    # y1data_H.append(y)
    time_text.set_text(time_template % (t))  # данные для вставки время
    temp_text.set_text(temp_template % (y))  # данные для вставки температуры
    # xdata_2.append(t)
    # ydata_2.append(y_2)
    xmin, xmax = ax.get_xlim()              # изменение масштаба по оси Х во времени
    if t >= xmax:
        ax.set_xlim(xmin+60, xmax+60)
        ax.figure.canvas.draw()
    line_T.set_data(xdata_T, ydata_T)
    # line_2.set_data(xdata_2, ydata_2)
    return line_T,

# # функция для обновления графика
# def run1(data):
#     # print(data)
#     # print(ani)
#     # update the data
#     # t, y, y_2 = data
#     t, y, = data                          # связан с выходом функции data_gen  yield t, (cnt)
#     x1data_H.append(t)
#     y1data_H.append(y)
#     time_text.set_text(time_template % (t))  # данные для вставки время
#     temp_text.set_text(temp_template % (y))  # данные для вставки время
#     # xdata_2.append(t)
#     # ydata_2.append(y_2)
#     xmin, xmax = ax.get_xlim()              # изменение масштаба по оси Х во времени
#     if t >= xmax:
#         ax.set_xlim(xmin+60, xmax+60)
#         ax.figure.canvas.draw()
#     line_T.set_data(xdata_T, ydata_T)
#     # line_2.set_data(xdata_2, ydata_2)
#     return line_T,

# функция генерации данных для графика
def data_gen(t=0):
    data_gen_T = 0
    data_gen_H = 0
    while data_gen_T < 1000:
        if not pause:               # пока не нажата пауза генирировать данные
            data_gen_T = np.random.randint(10, 40)          # генерация данных для ТЕМПЕРАТУРЫ
            data_gen_H = np.random.randint(20, 80)          # генерация данных для ВЛАЖНОСТИ
            t += 1
        yield t, data_gen_T, data_gen_H             # на выходе время и значение температуры, влажности
                                                    # - является входом для  функции run

# # функция генерации данных для графика
# def data_gen1(t=0):
#     data_gen_H = 0
#     while data_gen_H < 1000:
#         if not pause:
#             data_gen_H = np.random.randint(10, 30)
#             t += 1
#         yield t, data_gen_H  # на выходе время и значение температуры

# функция оставноки анимации графика

# функция заморозки графика
i = 0
def onClick():
    global pause, i
    pause ^= True       # pause = pause ^ True, где ^ - XOR
    B4.configure(text="Возобновить", background='green')
    if i == 1:
        B4.configure(text="Стоп", background='red')
        i = 0
        return
    i = 1

# time_template = 'Время = %.1f c'                             # вставка текста в график
# temp_template = 'Температура = %.1f C'                             # вставка текста в график
# time_text = ax.text(0.5, 0.5, '', transform=ax.transAxes)   # вставка текста в график
# temp_text = ax.text(0.5, 0.3, '', transform=ax.transAxes)   # вставка текста в график
fig.canvas.mpl_connect('button_release_event', onClick)

# fig.canvas.mpl_connect('button_press_event', onClick)
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=1000,
                                repeat=False, init_func=init)                        # анамация графика

# вывод кнопок в окно приложения
B1 = Button(labelTop, text="Cтарт", command=start)
B1.grid(column=0, row=0)          # pack() - по цетру размещает

# вывод кнопки Закрыть  в окно приложения
B2 = Button(labelTop, text='Закрыть', command=quit)
B2.grid(column=3, row=0)

# # вывод кнопки Закрыть  в окно приложения
# B3 = Button(labelTop, text='Старт_COM3', command=start_com)
# B3.grid(column=2, row=0)

# вывод кнопок в окно приложения
B4 = Button(labelTop, text="Cтоп", command=onClick, background='red')
B4.grid(column=1, row=0)          # pack() - по цетру размещает

root.mainloop()