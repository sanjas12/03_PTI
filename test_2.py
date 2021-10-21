import serial
from tkinter.ttk import *  # для combobox
import csv
from def_setup import *

# вызов функции создания и проверки существования csv файли и его размера
# из def_setup
my_filename = work_with_csv()
print(my_filename[0])               # вывод текущего файла в который будем записывать

# открытие порта ардуино    !!ПЕРЕД ФУНКЦИЯМИ
arduino = serial.Serial()
arduino.port = 'COM3'
arduino.timeout = 2
arduino.open()

# метка времни              !!ПЕРЕД ФУНКЦИЯМИ
time_stump_csv = time.strftime('%Y_%m_%d %H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_filename = time.strftime('%Y_%m_%d')        # год_месяц_день

# создание окна программы
root = Tk()
root.minsize(width=350, height=200)
root.title('тем_влаж')

# функция запись в csv с помощью библиотеки csv с кнопки "СТАРТ"
# open_port = 0                        #  0 - порт закрыт, 1 - порт открыт
# def start_write_csv():
#     open_port = 1
#     i = 0
#     with open('test_2.csv', 'a') as arduino_csv:  # так открывать файл лучше, через open питон для ардуино стр.150
#         w = csv.writer(arduino_csv, delimiter=';')  # запись в csv с помощью библиотеки csv
#         row_0 = (time_stump_csv, 'Дата', 'Влажность', 'Температура')  # 0 строка
#         w.writerow(row_0)  # запись сторки в файл csv
#         while i < 10:
#             data = arduino.readline()
#             data = str(data)
#             data_vlag = data[5:7]
#             data_temp = data[17:19]
#             row_data = (time.strftime('%Y_%m_%d %H:%M:%S'), data_vlag, data_temp)
#             w.writerow(row_data)
#             print('T:', data_temp, 'H:', data_vlag, '___', time.strftime('%Y_%m_%d %H:%M:%S'))
#             i += 1
#             time.sleep(int(menu_sec.get()))
#     return (data_temp, data_vlag,)




# функция_2 запись в csv с помощью библиотеки csv с кнопки "СТАРТ"
# open_port = 0                        #  0 - порт закрыт, 1 - порт открыт
def start_write_csv():
    i = 0
    global my_filename
    while i < 10:
        dd = start_view_data()
        lab_vlag.config(text=dd[0])
        lab_temp.config(text=dd[1])
        with open(my_filename[0], 'a', newline='') as ard_csv:  # так открывать файл лучше, через open питон для ардуино стр.150
            w = csv.writer(ard_csv, delimiter=';')  # запись в csv с помощью библиотеки csv в качестве раздилителя - ;
                                                    # newline='' - правильно сохраняет в csv
            row_data = (time.strftime('%Y_%m_%d %H:%M:%S'), dd[0], dd[1])
            w.writerow(row_data)
        print('T:', dd[1], 'H:', dd[0], '___', time.strftime('%Y_%m_%d %H:%M:%S'))
        i += 1
        time.sleep(int(menu_sec.get()))
    return()

# функция считыванич данных-ардуино из функции start_view_data
def start_view_data():
    time.sleep(2)
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

# функия обновления температуры и влажности в окне программы и принудительной записи в csv
def refresh():
    time.sleep(1)
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

# Вывод текста в окно программы
lab03 = Label(root, text="Температура", font="Arial 14")
lab09 = Label(root, text="Влажность", font="Arial 14")
lab03.place(x=40, y=10)
lab09.place(x=190, y=10)
lab_C = Label(root, text="C", font="Arial 12")
lab_persent = Label(root, text="%", font="Arial 12")
lab_C.place(x=120, y=50)
lab_persent.place(x=260, y=50)

# Вывод текста ЧАСТОТА
lab_chastota = Label(root, text="Частота записи в csv, с", font="Arial 11")
lab_chastota.place(x=0, y=120)

# создание рамок для температуры и влажности  для случая listbox
# list_vlag = Listbox(root, width=3, height=1)
# list_vlag.place(x=75, y=50)
# list_temp = Listbox(root, width=3, height=1)
# list_temp.place(x=215, y=50)

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
lab_time = Label(root, text=l3, font="Arial 9")
lab_time.place(x=245, y=77)
lab_hour = Label(root, text=l4, font="Arial 9")
lab_hour.place(x=245, y=96)

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(root, values=spisok_t, width=2, height=11)
menu_sec.place(x=220, y=120)
menu_sec.insert(0, spisok_t[1])     # по дефолту ставим 60 сек

# для включения и остановки
button_status_B1 = 0       # 0 - запись выключена, 1 - запись включена,
button_status_B2 = 0
def B1_on():
    global button_status_B1
    button_status_B1 = 0
    print('b1:', button_status_B1, 'b2:', button_status_B2)

def B1_off():
    global button_status_B1
    button_status_B1 = 1
    print('b1:', button_status_B1, 'b2:', button_status_B2)

# вывод кнопок в окно приложения
B1 = Button(root, text="старт", command=start_write_csv)
B1.place(x=150, y=150)          # pack() - по цетру размещает

B2 = Button(root, text="обновить", command=refresh)
B2.place(x=130, y=80)          # pack() - по цетру размещает

root.mainloop()