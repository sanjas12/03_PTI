import threading                    # для многопоточности
                                    # http://asvetlov.blogspot.ru/2010/11/1.htmlhttp://asvetlov.blogspot.ru/2010/11/1.html
import csv
from tkinter.ttk import *           # для combobox
from def_setup import *

import serial

# создание окна программы
root = Tk()
root.minsize(width=350, height=200)
root.title('тем_влаж')

# открытие порта ардуино    !!ПЕРЕД ФУНКЦИЯМИ
arduino = serial.Serial()
arduino.port = 'COM4'
arduino.timeout = 2
arduino.open()

i = 0

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(root, values=spisok_t, width=2, height=11)
menu_sec.place(x=220, y=80)
menu_sec.insert(0, spisok_t[0])     # по дефолту ставим 60 сек

bit_start = 1

my_filename = work_with_csv()

def printit():
    global bit_start, my_filename
    B1.configure(state=DISABLED, command=B1_off())
    while bit_start:
        data = start_view_data_pti()
        # print(type(data))
        # print(len(data))
        # print(data[0], data[1])
        with open(my_filename[0], 'a', newline='') as ard_csv:  # так открывать файл лучше, через open питон для ардуино стр.150
            w = csv.writer(ard_csv, delimiter=';')  # запись в csv с помощью библиотеки csv в качестве раздилителя - ;
                                                    # newline='' - правильно сохраняет в csv
            row_data = (time.strftime('%Y_%m_%d %H:%M:%S'), data[0], data[1])
            w.writerow(row_data)
        print('T:', data[0], 'H:', data[1], '___', time.strftime('%Y_%m_%d %H:%M:%S'))
        threading.Timer(int(menu_sec.get()), printit).start()
        return

# def refresh():
#     printit()
#     th1 = threading.Timer(5, printit)
#     # threading.Timer(int(menu_sec.get()), printit).start()
#     th1.start()

def stop():
    global bit_start
    # threading.Timer(int(menu_sec.get()), printit).cancel()
    B1.configure(state=ACTIVE, command=B1_on())
    bit_start = 0
    # th1.cancel()

button_status_B1 = 0       # 0 - запись выключена, 1 - запись включена,
button_status_B2 = 0

# функция блокировки кнопки "старт"
def B1_off():
    B1.configure(state=ACTIVE, command=B1_on())
    global button_status_B1
    button_status_B1 = 1
    # print('b1:', button_status_B1, 'b2:', button_status_B2)

# функция деблокировки кнопки "старт"
def B1_on():
    global button_status_B1, bit_start
    button_status_B1 = 0
    # print('b1:', button_status_B1, 'b2:', button_status_B2)
    # bit_start = 0

# функция считыванич данных-ардуино из функции start_view_data
def start_view_data():
    time.sleep(2)
    data = arduino.readline()
    data = str(data)
    print(data)
    print (len(data))
    data_vlag = data[5:7]
    data_temp = data[17:19]
    if data_temp and data_vlag:
        print(data_temp, data_vlag, time.strftime('%Y_%m_%d %H:%M:%S'))
    else:
        print('нет данных')
    return (data_temp, data_vlag)

# функция считыванич данных-ардуино из функции start_view_data
def start_view_data_pti():
    time.sleep(2)
    data = arduino.readline()
    data = data.decode()                        # преобразование бит в str
    print(data)
    print(len(data))
    print(type(data))
    data_temp = data[5:7]
    data_vlag = data[17:19]
    if data_temp and data_vlag:
        print(data_temp, data_vlag, time.strftime('%Y_%m_%d %H:%M:%S'))
    else:
        print('нет данных')
    print('*'*10)
    return (data_temp, data_vlag)

# вывод кнопок в окно приложения
B1 = Button(root, text="старт", command=printit)
B1.place(x=150, y=120)          # pack() - по цетру размещает

B2 = Button(root, text="стоп", command=stop)
B2.place(x=250, y=120)          # pack() - по цетру размещает

root.mainloop()


# Поток - прервать нельзя. Процесс - можно.
# В питоне есть модуль processing - попробуй его заюзать.
# Хотя можешь порыскать по сети - я находил рецепты-извращения,
# связаные, например, с пропихиванием исключения внутрь потока,
# но всё равно с атомарными операциями это не прокатит
# http://python.su/forum/topic/9463/?page=1#post-61215
