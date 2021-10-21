import threading                    # для многопоточности
import serial                           # http://asvetlov.blogspot.ru/2010/11/1.htmlhttp://asvetlov.blogspot.ru/2010/11/1.html
from tkinter.filedialog import *    # для os.path и для TK()
from tkinter.ttk import *           # для combobox
import random
import time

# метка времни              !!ПЕРЕД ФУНКЦИЯМИ
time_stump_csv = time.strftime('%Y_%m_%d %H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_filename = time.strftime('%Y_%m_%d')        # год_месяц_день

# создание окна программы
root = Tk()
root.minsize(width=350, height=200)
root.title('ПТИ')

# создание списка частоты записи
spisok_com = ['COM3', 'COM4',]        # выбор частоты записи
menu_com = Combobox(root, values=spisok_com, width=6, height=11)
menu_com.place(x=220, y=160)
menu_com.insert(0, spisok_com[0])     # по дефолту ставим 60 сек

# открытие порта ардуино    !!ПЕРЕД ФУНКЦИЯМИ
arduino = serial.Serial()
arduino.port = menu_com.get()
arduino.timeout = 2

# функция запуска ПТИ
def start():
    arduino.open()
    data_temp = 25
    data_vlag = 50
    delta_temp = random.randint(-5, 5)
    delta_vlag = random.randint(-10, 10)
    data_temp = data_temp + delta_temp
    data_vlag = data_vlag + delta_vlag
    data = 'кенгш' + str(data_temp) + 'рррytgherr' + str(data_vlag) + 'ytg' +'\0' # длина должна быть - 31
    data_temp_2 = data[5:7]
    data_vlag_2 = data[17:19]
    lab_vlag.config(text=data_temp_2)              # вставляет тектс в окно программы
    lab_temp.config(text=data_vlag_2)
    data_b = data.encode()                          # преобразуем в биты
    arduino.write(data.encode('utf-8'))             # отправляем в COM порт
    threading.Timer(int(menu_sec.get()), start).start()
    arduino.close()

# функция закрытия приложения
def quit():
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(root, values=spisok_t, width=2, height=11)
menu_sec.place(x=220, y=90)
menu_sec.insert(0, spisok_t[0])     # по дефолту ставим 60 сек

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
lab_chastota = Label(root, text="Частота обновление, с", font="Arial 11")
lab_chastota.place(x=0, y=90)


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
B1 = Button(root, text="старт", command=start)
B1.place(x=150, y=120)          # pack() - по цетру размещает

# вывод кнопки Закрыть  в окно приложения
B2 = Button(master=root, text='Закрыть', command=quit)
B2.place(x=50, y=120)

root.mainloop()