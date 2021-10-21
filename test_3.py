import threading                    # для многопоточности
                                    # http://asvetlov.blogspot.ru/2010/11/1.htmlhttp://asvetlov.blogspot.ru/2010/11/1.html
import csv
from tkinter.ttk import *           # для combobox
import serial
from def_setup import *

# создание окна программы
root = Tk()
root.minsize(width=360, height=200)
root.title('тем_влаж')

# открытие порта ардуино    !!ПЕРЕД ФУНКЦИЯМИ
arduino = serial.Serial()
arduino.port = 'COM4'
arduino.timeout = 1
arduino.open()

# вызов функции создания и проверки существования csv файли и его размера
# из def_setup и присвоения переменной my_filename - имя файла который будет использован для записи
my_filename = work_with_csv()
# print(my_filename[0])               # вывод текущего файла в который будем записывать

# метка времни              !!ПЕРЕД ФУНКЦИЯМИ
time_stump_csv = time.strftime('%Y_%m_%d %H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_filename = time.strftime('%Y_%m_%d')        # год_месяц_день

i = 0

# создание списка частоты записи
y3 = 160
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(root, values=spisok_t, width=2, height=11)
menu_sec.place(x=180, y=y3)
menu_sec.insert(0, spisok_t[3])     # по дефолту ставим 60 сек

# Вывод текста ЧАСТОТА ЗАПИСИ в csv
lab_chastota = Label(root, text="Частота записи в csv, с", font="Arial 11")
lab_chastota.place(x=0, y=y3)

# Вывод текста в окно программы
lab03 = Label(root, text="Температура", font="Arial 14")
lab09 = Label(root, text="Влажность", font="Arial 14")
lab03.place(x=40, y=10)
lab09.place(x=190, y=10)
lab_C = Label(root, text="C", font="Arial 12")
lab_persent = Label(root, text="%", font="Arial 12")
lab_C.place(x=120, y=50)
lab_persent.place(x=260, y=50)

# создание текста для температуры и влажности
l1 = '--'
l2 = '--'
l3 = time_stump_filename
l4 = time.strftime('%H:%M:%S')
font_lab = "Arial 12"
lab_vlag = Label(root, text=l1, font=font_lab)
lab_vlag.place(x=85, y=50)
lab_temp = Label(root, text=l2, font=font_lab)
lab_temp.place(x=225, y=50)
lab_time = Label(root, text=l3, font="Arial 9")
lab_time.place(x=260, y=77)
lab_hour = Label(root, text=l4, font="Arial 9")
lab_hour.place(x=260, y=96)

bit_start = 1

# функция записи в csv-файл с изменяемой частотой, которая берется из Сombobox
def start_write():
    global bit_start, my_filename
    B1.configure(state=DISABLED, command=B1_off())
    global i
    while bit_start:
        with open(my_filename[0], 'a', newline='') as ard_csv:          # так открывать файл лучше, через open питон для ардуино стр.150
                                                                      # newline='' - правильно сохраняет в csv
            w = csv.writer(ard_csv, delimiter=';')        # запись в csv с помощью библиотеки csv в качестве раздилителя - ;
            dd = start_view_data()
            row_data = (time.strftime('%Y_%m_%d %H:%M:%S'), dd[0], dd[1])
            w.writerow(row_data)                          # запись сторки в файл csv
            print('записал в csv в:', time.strftime('%Y_%m_%d %H:%M:%S'))
        i += 1
        threading.Timer(int(menu_sec.get()), start_write).start()
        return

# функция деблокировки кнопки "старт"
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

# функия обновления температуры и влажности в окне программы и принудительной записи в csv
def refresh():
    global my_filename
    if True:
        dd = start_view_data()      # считывание данных-ардуино из функции start_view_data
        # list_vlag.delete(0)  #         если listbox, то так выводим туда инфу
        # list_temp.delete(0)  #
        # list_vlag.insert(0, dd[0])
        # list_temp.insert(0, dd[1])                                #
        lab_vlag.config(text=dd[0])
        lab_temp.config(text=dd[1])
        lab_time.config(text=time.strftime('%Y_%m_%d'))
        lab_hour.config(text=time.strftime('%H:%M:%S'))
        if len(dd[0]) == 0:                       # если нет данных с ардуино, то пишем прочерки
            lab_vlag.config(text=l1)
            lab_temp.config(text=l2)
        lab_vlag.update_idletasks()
        with open(my_filename[0], 'a', newline='') as ard_csv:  # так открывать файл лучше, через open питон для ардуино стр.150
            w = csv.writer(ard_csv, delimiter=';')  # запись в csv с помощью библиотеки csv в качестве раздилителя - ;
            row_data = (time.strftime('%Y_%m_%d %H:%M:%S'), dd[0], dd[1], 'обновить')
            w.writerow(row_data)                     # запись сторки в файл csv
            print('записал в csv')
        print('обновил')
    else:
        print('______3')
    return ()

# функция считыванич данных-ардуино из функции start_view_data
def start_view_data():
    data = arduino.readline()
    data = str(data)
    print(data)
    data_vlag = data[5:7]
    data_temp = data[17:19]
    if data_temp and data_vlag:
        print(data_temp, data_vlag, time.strftime('%Y_%m_%d %H:%M:%S'))
    else:
        print('нет данных')
    return (data_temp, data_vlag)

# функция закрытия приложения
def quit():
    arduino.close()
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# вывод кнопок в окно приложения
B1 = Button(root, text="старт", command=start_write)
B1.place(x=220, y=160)          # pack() - по цетру размещает

B2 = Button(root, text="стоп", command=stop)
B2.place(x=280, y=160)          # pack() - по цетру размещает

B3 = Button(root, text="обновить", command=refresh)
B3.place(x=130, y=80)          # pack() - по цетру размещает

# вывод кнопки Закрыть  в окно приложения
B4 = Button(root, text='Закрыть', command=quit)
B4.place(x=300, y=120)

root.mainloop()


# Поток - прервать нельзя. Процесс - можно.
# В питоне есть модуль processing - попробуй его заюзать.
# Хотя можешь порыскать по сети - я находил рецепты-извращения,
# связаные, например, с пропихиванием исключения внутрь потока,
# но всё равно с атомарными операциями это не прокатит
# http://python.su/forum/topic/9463/?page=1#post-61215
