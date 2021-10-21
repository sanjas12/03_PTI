from tkinter.filedialog import *
import time
import serial
from tkinter.ttk import *  # для combobox

# метка времни
time_stump = time.strftime('%Y_%m_%d %H:%M:%S')    # год_месяц_день_час_минута_сек
time_stump_file = time.strftime('%Y_%m_%d')        # год_месяц_день

# создание окна приложения
root = Tk()
root.minsize(width=350, height=200)
root.title('тем_влаж')

# открытие порта ардуино
arduino = serial.Serial()
arduino.port = 'COM3'
arduino.timeout = 2
arduino.open()

# создание рамок для температуры и влажности
list_vlag = Listbox(root, width=5, height=1)
list_vlag.place(x=40 + 35, y=10 + 40)
list_temp = Listbox(root, width=5, height=1)
list_temp.place(x=40 + 175, y=10 + 40)

# Вывод текста в окно программы
lab03 = Label(root, text="Температура", font="Arial 14")
lab09 = Label(root, text="Влажность", font="Arial 14")
lab_chastota = Label(root, text="Частота записи, с", font="Arial 11")
lab03.place(x=40, y=10)
lab09.place(x=40 + 150, y=10)
lab_chastota.place(x=20, y=120)


# запись в csv с помощью по дефолту
def start_write_csv():                              # event надо писать если эта функция будет использоваться с кнопки
    B1.configure(state=DISABLED, command=B1_off())
    while button_status_B1 == 1:
        data = arduino.readline()
        data = str(data)                # длина data - 31 символ
        data_vlag = data[5:7]
        data_temp = data[17:19]
        data_vlag = int(float(data_vlag))
        insert_T_H(data_vlag, data_temp)
        print('T:', data_temp, 'H:', data_vlag, '___', time.strftime('%Y_%m_%d %H:%M:%S'))

def stop_write_csv():    # event надо писать если эта функция будет использоваться с кнок
    B1.configure(state=ACTIVE, command=B1_on())
    arduino.close()

def insert_T_H(data_vlag, data_temp):
    list_vlag.insert(0, 9)
    list_vlag.delete(0)  #
    list_temp.delete(0)  #
    list_vlag.insert(0, data_vlag)  # вставка влажности в 0 строку
    list_temp.insert(0, data_temp)  # вставка темепературы в 1 строку
    return data_temp, data_vlag

# создание списка частоты записи
spisok_t = [1, 5, 10, 60, 600]        # выбор частоты записи
menu_sec = Combobox(root, values=spisok_t, width=2, height=11)
menu_sec.place(x=180, y=120)
menu_sec.insert(0, spisok_t[1])     # по дефолту ставим 60 сек

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

def B2_on():
    global button_status_B2
    button_status_B2 = 1
    print('b2:', button_status_B2,  'b2:', button_status_B2)

def B2_off():
    global button_status_B2
    button_status_B2 = 2
    print('b2:', button_status_B2,  'b2:', button_status_B2)

B1 = Button(root, text="старт", command = start_write_csv)
B1.place(x=150, y=150)          # pack() - по цетру размещает

B2 = Button(root, text="стоп", command = stop_write_csv)
B2.place(x=250, y=150)          # pack() - по цетру размещает

root.mainloop()