import threading                    # для многопоточности
import serial                           # http://asvetlov.blogspot.ru/2010/11/1.htmlhttp://asvetlov.blogspot.ru/2010/11/1.html
from tkinter.ttk import *           # для combobox
import random
import time
from tkinter.filedialog import *    # для окна приложения и для TK()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt                  # для анимации
import matplotlib.animation as animation            # для анимации
import numpy as np
from matplotlib.figure import Figure

# метка времни              !!ПЕРЕД ФУНКЦИЯМИ
time_stump_csv = time.strftime('%Y_%m_%d %H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_filename = time.strftime('%Y_%m_%d')        # год_месяц_день

# создание окна программы
root = Tk()
# root.minsize(width=700, height=600)
root.title('ПТИ')

# создание контенера для кнопок, комбобокса и т.д.
labelTop = LabelFrame(root, text='')
labelTop.grid(column=0, row=2)
# labelFrame.place(x=200, y=70)
Label(labelTop, text='частота обновления, с').grid(column=1, row=2)

# создание контенера для графика ТЕМПЕРАТУРА
labelGrath_T = LabelFrame(root, text='')
labelGrath_T.grid(column=0, row=0)

# создание контенера для графика ВЛАЖНОСТЬ
labelGrath_H = LabelFrame(root, text='')
labelGrath_H.grid(column=0, row=1)

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(labelTop, values=spisok_t, width=2, height=11)
menu_sec.grid(column=2, row=2)
menu_sec.insert(0, spisok_t[0])     # по дефолту ставим 60 сек

# создание 1 графика ТЕМПЕРАТУРА
fig, ax, = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
line_T, = ax.plot([], [], color='blue', ls='solid', lw=1.5)          # линия для графика Температуры
ax.grid()
# ax.pack()
fig.set_size_inches(6.0, 2.0)
ax.set_title('Температура')                 # название графика
ax.set_xlabel('время')                       # название оси
# ax.set_ylabel('температура')
xdata_T, ydata_T = [], []                   # массив данных для X и Y для 1 графика
ax.set_ylim(10, 40)  # лимиты по оси Y
ax.set_xlim(0, 60)  # лимиты по оси Y
time_template = 'Time = %.1f s'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# отрисовка осей и подписей к 1 графику
canvas = FigureCanvasTkAgg(fig, master=labelGrath_T)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # положение окна с осями
time_template = 'Время = %.1f c'                             # вставка текста в график
temp_template = 'Температура = %.1f C'                             # вставка текста в график
time_text = ax.text(0.5, 0.5, '', transform=ax.transAxes)   # вставка текста в график
temp_text = ax.text(0.5, 0.3, '', transform=ax.transAxes)   # вставка текста в график

# создание 2 графика ВЛАЖНОСТЬ
fig1, ax1, = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
line_H = ax1.plot([], [], color='blue', ls='solid', lw=1.5)
ax1.grid()
fig1.set_size_inches(6.0, 2.0)
ax1.set_title('Влажность')                 # название графика
ax1.set_xlabel('время')                       # название оси
# ax1.set_ylabel('температура')
x1data_H, y1data_H = [], []
ax1.set_ylim(20, 80)  # лимиты по оси Y
ax1.set_xlim(0, 60)  # лимиты по оси Y

# отрисовка осей и подписей к 2 графику
canvas1 = FigureCanvasTkAgg(fig1, master=labelGrath_H)
canvas1.show()
canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # положение окна с осями

# функция запуска ПТИ
def start():
    data_temp = 25 + random.randint(-5, 5)
    data_vlag = 50 + random.randint(-10, 10)
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    # ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=int(menu_sec.get()),
    #                               repeat=False, init_func=init)
    # threading.Timer(int(menu_sec.get()), start).start()
    return (data_vlag, data_temp)

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

# функция для обновления данных для графика
def run(data):
    print(data)
    # update the data
    # t, y, y_2 = data
    t, y, = data                          # связан с выходом функции data_gen  yield t, (cnt)
    xdata_T.append(t)
    ydata_T.append(y)
    time_text.set_text(time_template % (t))
    # xdata_2.append(t)
    # ydata_2.append(y_2)
    xmin, xmax = ax.get_xlim()              # изменение масштаба по оси Х во времени
    if t >= xmax:
        ax.set_xlim(xmin+60, xmax+60)
        ax.figure.canvas.draw()
    line_T.set_data(xdata_T, ydata_T)
    # line_2.set_data(xdata_2, ydata_2)
    return line_T,

# функция генерации данных для графика
pause = False
def data_gen(t=0):
    data_gen_T = 0
    while data_gen_T < 1000:
        if not pause:
            data_gen_T = np.random.randint(10, 30)
            # cnt_2 = np.random.randint(30, 80)
            t += 1
            # lab_vlag.config(text=cnt)
            # lab_temp.config(text=cnt_2)
            # yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
        yield t, data_gen_T                                       # на выходе время и значение температуры

# функция оставноки анимации графика
def onClick(event):
    global pause
    pause ^= True

fig.canvas.mpl_connect('button_press_event', onClick)     # остановка анимации графика
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=1000,
                               repeat=False, init_func=init)                        # анамация графика

# вывод кнопок в окно приложения
B1 = Button(labelTop, text="Cтарт", command=start)
B1.grid(column=0, row=0)          # pack() - по цетру размещает

# вывод кнопок в окно приложения
B1 = Button(labelTop, text="Cтоп", command=pause)
B1.grid(column=0, row=0)          # pack() - по цетру размещает

# вывод кнопки Закрыть  в окно приложения
B2 = Button(labelTop, text='Закрыть', command=quit)
B2.grid(column=1, row=0)

# вывод кнопки Закрыть  в окно приложения
B3 = Button(labelTop, text='Старт_COM3', command=start_com)
B3.grid(column=2, row=0)

root.mainloop()