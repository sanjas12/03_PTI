from tkinter.filedialog import *    # для os.path
import time

# функция выбора csv файла для записи данных с ардуино и проверка размера файла
def work_with_csv():
    time_stump_file = time.strftime('%Y_%m_%d')
    for_file = ['_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', '_10']
    i = 0
    file_size = 2000                                                     # размер файла в кб
    for zz in for_file:
        filename = time_stump_file + '_data' + for_file[i] + '.csv'
        if i < len(for_file) and os.path.exists(filename) and os.path.getsize(filename) < file_size:
            print('Файл_', filename, ' уже есть и он < ', file_size, 'кб')
            break
        elif os.path.exists(filename) and os.path.getsize(filename) > file_size:
            print('Файл_', filename, ' > ', file_size, 'кб')
            filename = time_stump_file + '_data' + for_file[i + 1] + '.csv'
            print('Файл_', filename, ' создан из-за превышения размера')
            outfile1 = open(filename, 'a')
            if os.path.getsize(filename) == 0:
                outfile1.write('Дата' + ';' + 'Влажность' + ';' + 'Температура' + ';' + "\n")
            break
        else:
            filename = time_stump_file + '_data' + for_file[i] + '.csv'
            print('Файл_', filename, ' создан ')
            outfile1 = open(filename, 'a')
            if os.path.getsize(filename) == 0:
                outfile1.write('Дата' + ';' + 'Влажность' + ';' + 'Температура' + ';' + "\n")
            break
        i += 1
    print('Запись будет в', filename)
    return filename, i
