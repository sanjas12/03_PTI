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
root.minsize(width=700, height=600)
root.title('ПТИ')

# создание контейнера для кнопок, комбобокса и т.д.
labelTop = LabelFrame(root, text='ПТИ')
labelTop.grid(column=0, row=0)
# labelFrame.place(x=200, y=70)
# Label(labelTop, text='1').grid(column=0, row=0)

# создание контейнера для графиков
labelGrath = LabelFrame(root, text='Графики')
labelGrath.grid(column=1, row=1)
# labelFrame.place(x=200, y=70)
# Label(labelTop, text='1').grid(column=0, row=0)


# создание списка частоты записи
spisok_com = ['COM3']        # выбор частоты записи
menu_com = Combobox(labelTop, values=spisok_com, width=6, height=11)
# menu_com.place(x=220, y=160)
menu_com.grid(column=0, row=1)
menu_com.insert(0, spisok_com[0])     # по дефолту ставим 60 сек

# открытие порта ардуино    !!ПЕРЕД ФУНКЦИЯМИ
PTI_COM = serial.Serial()
PTI_COM.port = menu_com.get()
PTI_COM.timeout = 2

# создаине 1 и 2 графика
# fig, ax,  = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
# fig2, ax2,  = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
fig = Figure(figsize=(1, 1), dpi=100)
ax = fig.add_subplot(111)
fig.set_size_inches(2.0, 2.0)
# fig2 = Figure(figsize=(2, 2), dpi=100)
# ax2 = fig2.add_subplot(122)
line, = ax.plot([], [], color='blue', ls='solid', lw=1.5)
line_2, = ax.plot([], [], color='red', ls='solid', lw=1.5)      # вид, тип, цвет графика lw-толшина линии
fig.legend((line_2, line,), ('Влаж:', 'Tем:',), loc=(0.2, 0.2), shadow=True)  # создание легенды


# fig, ax, = plt.subplots()     # создание октивного окна (fig) и области построение графиков (ax)
# line, = ax.plot([], [], color='blue', ls='solid', lw=1.5)
# line_2, = ax.plot([], [], color='red', ls='solid', lw=1.5)      # вид, тип, цвет графика lw-толшина линии
# fig.legend((line_2, line,), ('Влаж:', 'Tем:',), loc=(0.2, 0.2), shadow=True)  # создание легенды
# # fig.legend((line_2),(line), ('Tем:'), ('Влаж:'), loc=(0.5, 0.5), loc=(0.2, 0.2))  # создание легенды
# # fig.legend_2((line), ('Tем:'), loc=(0.2, 0.2), shadow=True)  # создание легенды
# # fig.set_size_inches(2.0, 2.0)

ax.grid()
ax.set_title('Tk embedding')                 # название графика
ax.set_xlabel('время')                       # название оси
ax.set_ylabel('температура, влажность')
xdata, ydata = [], []                   # массив данных для X и Y для 1 графика
xdata_2, ydata_2 = [], []               # массив данных для X и Y для 2 графика

# отрисовка осей и подписей к ним
canvas = FigureCanvasTkAgg(fig, master=labelGrath)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # положение окна с осями

# отрисовка инструментов для работы с графикой
toolbar = NavigationToolbar2TkAgg(canvas, labelGrath)
toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

# функция запуска ПТИ
def start():
    data_temp = 25 + random.randint(-5, 5)
    data_vlag = 50 + random.randint(-10, 10)
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=int(menu_sec.get()),
                                  repeat=False, init_func=init)
    threading.Timer(int(menu_sec.get()), start).start()
    return (data_vlag, data_temp)

# функция запуска ПТИ в сом порт
def start_com():
    PTI_COM.open()
    data_temp = 25 + random.randint(-5, 5)
    data_vlag = 50 + random.randint(-10, 10)
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    PTI_COM.write(data.encode('utf-8'))             # отправляем в COM порт
    PTI_COM.close()
    threading.Timer(int(menu_sec.get()), start_com).start()

# функция закрытия приложения
def quit():
    PTI_COM.close()
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# функция генерации данных для графика
def data_gen(t=0):
    cnt = 0
    while cnt < 1000:

        cnt = np.random.randint(10, 30)
        cnt_2 = np.random.randint(30, 80)
        t += 0.5
        lab_vlag.config(text=cnt)
        lab_temp.config(text=cnt_2)
        # yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
        yield t, (cnt), (cnt_2),

# функция для начального состояния графика
def init():
    ax.set_ylim(0, 100)                 # лимиты по оси Y
    ax.set_xlim(0, 60)                 # лимиты по оси Y
    del xdata[:]                        # очистка массива исходных данных для X для 1 графика
    del ydata[:]                        # очистка массива исходных данных для Y для 1 графика
    del xdata_2[:]                      # очистка массива исходных данных для X для 2 графика
    del ydata_2[:]                      # очистка массива исходных данных для Y для 2 графика
    line.set_data(xdata, ydata)         # в качестве данных для 1 графика будут xdata и ydata
    line_2.set_data(xdata_2, ydata_2)     # в качестве данных для 1 графика будут xdata и ydata
    return line, line_2,

# функция для обновления графика
def run(data):
    # update the data
    t, y, y_2 = data
    xdata.append(t)
    ydata.append(y)
    xdata_2.append(t)
    ydata_2.append(y_2)
    xmin, xmax = ax.get_xlim()              # изменение масштаба по оси Х во времени
    if t >= xmax:
        ax.set_xlim(xmin+60, xmax+60)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)
    line_2.set_data(xdata_2, ydata_2)
    return line, line_2,

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(labelTop, values=spisok_t, width=2, height=11)
menu_sec.grid(column=0, row=2)
menu_sec.insert(0, spisok_t[0])     # по дефолту ставим 60 сек

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=1000*int(menu_sec.get()),
                               repeat=False, init_func=init)

# Вывод текста в окно программы
lab03 = Label(root, text="Температура", font="Arial 14")
lab09 = Label(root, text="Влажность", font="Arial 14")
lab03.place(x=40, y=10)
lab09.place(x=40 + 150, y=10)
lab_C = Label(root, text="C", font="Arial 12")
lab_persent = Label(root, text="%", font="Arial 12")
lab_C.place(x=120, y=50)
lab_persent.place(x=260, y=50)

# Вывод текста ЧАСТОТА
lab_chastota = Label(root, text="Частота обновление COM, с", font="Arial 11")
lab_chastota.place(x=0, y=90)

labelFrame = LabelFrame(root, text='sds')
# labelFrame.grid(column=0, row=7)
labelFrame.place(x=200, y=70)

# создание текста для температуры и влажности
l1 = '--'
l2 = '--'
l3 = time_stump_filename
l4 = time.strftime('%H:%M:%S')
font_lab="Arial 12"
lab_vlag = Label(root, text=l1, font=font_lab)
lab_vlag.place(x=85, y=50)
lab_temp = Label(root, text=l2, font=font_lab)
lab_temp.place(x=225, y=50)

# вывод кнопок в окно приложения
B1 = Button(root, text="Cтарт", command=start)
B1.place(x=150, y=120)          # pack() - по цетру размещает

# вывод кнопки Закрыть  в окно приложения
B2 = Button(root, text='Закрыть', command=quit)
B2.place(x=250, y=120)

# вывод кнопки Закрыть  в окно приложения
B3 = Button(root, text='Старт_COM3', command=start_com)
B3.place(x=350, y=120)

root.mainloop()