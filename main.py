# место для библиотек и отдельных функций из них
from queue import PriorityQueue     # подключение класса PriorityQueue из библиотеки queue
import pickle                       # подключение библеотеки pickle с утилитой для сохрания объектов в файл 

class Node:                     # создание класса Node для постояния бинарного дерева
    def __init__(self) -> None: # создание конструктора класса Node (вызывается при создании узла бинарного дерева)
        self.symbol = None      # создание переменой symbol класса Node (равна None если не является конечной вершиной)
        self.left = None        # создание переменой left класса Node (левой ветви узла бинарного дерева)
        self.right = None       # создание переменой right класса Node (правой ветви узла бинарного дерева)
        
    def __lt__(self, other):    # переопределение оператора "больше", необходимого для работы приоритетной очереди
        return True             # всегда возвращает True (может вызывать ошибки, если TODO...)

def scan(node, code, dictionary):                                                                   # рекурсивная функция поиска в глубину по бинарному дереву для создания таблицы Хаффмана
    if node.symbol ==  None :                                                                       # если вершина НЕ КОНЕЧНА то продолжается поиск в глубину (сначала по левой ветви, затем по правой)
        scan(node.left, code + "1", dictionary)                                                     # сначала продолжение поиска в глубину по левой ветви
        scan(node.right, code + "0", dictionary)                                                    # затем по правой
    else :                                                                                          # если вершина КОНЕЧНА то записывается вершина с бинарным кодом в таблицу Хаффмана (с выводом в консоль)
        if node.symbol == '\n' :                                                                    # если выводимый символ - символ переноса строки 
            print("\'\\n\': ", code[::-1], " (", int(code[::-1], 2), ")", sep='')                   # последовательный вывод символа переноса строки, перевернутого (так как код генерируется с конца) кода этого символа через ":", затем десятичного варианта этого кода в "()"   
        else:                                                                                       # если выводимый символ - любой прочий символ
            print("\'", node.symbol, "\' : ", code[::-1], " (", int(code[::-1], 2), ")", sep='')    # последовательный вывод прочих символов, перевернутых кодов этих символов через ":", затем десятичных вариантов этих кодов в "()"
        dictionary[node.symbol] = int(code[::-1], 2)                                                # добавление в словарь по ключу  TODO
    return dictionary                                                                               # возвращаемая таблица Хаффмана из функции

def generate_dictionary(file):                                      # TODO
    symbols = {} 
    dictionary = {}
    for symbol in file :
        if symbols.get(symbol) == None :
            symbols[symbol] = 1
        else :
            symbols[symbol] += 1

    queue = PriorityQueue()
    for k in symbols :
        temp = Node()
        temp.symbol = k
        queue.put((symbols.get(k), temp))
        #print(k)
    
    while queue.qsize() != 1 :
        handle = queue.get()
        handle_priority = handle[0]
        handle_value = handle[1] 
        new_node = Node()
        new_node.left = handle_value
        handle2 = queue.get()
        handle2_priority = handle2[0]
        handle2_value = handle2[1]
        new_node.right = handle2_value
        queue.put((handle_priority + handle2_priority, new_node))
    
    temp = queue.get()                                              
    return scan(temp[1], "", {})

def read_file(name, is_encodeed):                                                                   # функция чтения файла 
    link_code_txt = open(name, "rt", encoding = "utf-8-sig")                                        # открытие файла на чтение в текстовом режиме с текстом на русском или английском языке
    if is_encodeed:                                                                                 # если файл ЗАШИФРОВАН:
        temp = link_code_txt.read()                                                                 # копирование содержимого файла link_code_txt в переменную temp для возможножности закрытия этого файла
        link_code_txt.close()                                                                       # закрытие файла link_code_txt
        #return pickle.load(open(name, 'rb'))
        return list(map(int, list(filter(lambda x: not(x is None or x == ''), temp.split(',')))))   # коды в файле разделяются "," и переводятся в числовой формат, добавляются в одну строку и эта строка - возвращаемое значение
    else:                                                                                           # если файл НЕ ЗАШИФРОВАН:
        file = ''                                                                                   # все символы файла добавляются в одну строку и эта строка - возвращаемое значение
        for str_temp in link_code_txt:
            for char_temp in str_temp:
                file += char_temp
        link_code_txt.close()                                                                       # закрытие файла link_code_txt
        return file                                                                                 # возвращаемое значение

def encode(file, dictionary):                       # функция шифрования или расшифрования по таблице Хаффмана
    decoded_file = []                               # объявление массива decoded_file
    for temp in file:
        decoded_file.append(dictionary.get(temp))   # добавление новых значений в массив
    return decoded_file                             # (за-)расшифрованный массив - возвращаемое значение

def reverse_dictionary(dictionary):                 # функция для переворачивания таблицы Хаффмана
    reverse_dictionary = {}                         # объявление словаря reverse_dictionary
    print(dictionary)
    for temp in dictionary:                         # TODO
        reverse_dictionary[dictionary[temp]] = temp
    return reverse_dictionary                       # возвращение перевернтого словаря

def save_file(file, name, is_encoded):  # функция сохранения файла
    f = open(name, "w")                 # открытие файла на перезапись
    try:
        if is_encoded:                  # если файл ЗАШИФРОВАН то все коды сохраняются через ","                                                                         
            for temp in file:
                f.write((str)(temp))
                f.write(',')
        else:                           # если файл НЕ ЗАШИФРОВАН то расшифрованный текст сохраняется в файл
            for temp in file:
                f.write((str)(temp))
    finally:
        f.close()                       # закрытие файла

def save_dictionary(dictionary):                                # функция сохранения словаря в файл code_haffmaned.txt с помощью библеотеки pickle                                            
    pickle.dump(dictionary, open("haffman_dictionary.txt", 'wb'))

def load_dictionary():                                      # функция загрузки словаря из файла code_haffmaned.txt с помощью библеотеки pickle
    return pickle.load(open("haffman_dictionary.txt", 'rb'))

def main():                                                                                                 # объявление основной функции
    mode = int(input("Для шифрования файла введите 0\nДля расшифрования файла введите 1\nВыбор режима: "))  # 0 - зашифровать, 1 - расшифровать
    if mode == 0:                                                                                           # режим ШИФРОВАНИЯ файла
        file = read_file("code.txt", False)                                                                 # загрузка не зашифрованного файла
        dictionary = generate_dictionary(file)                                                              # создание словаря
        save_dictionary(dictionary)                                                                         # сохранение словаря
        save_file(encode(file, dictionary), "encoded.txt", True)                                            # шифрование и сохранение зашифрованного файла
    elif mode == 1:                                                                                         # режим РАСШИФРОВАНИЯ файла
        file = read_file("encoded.txt", True)                                                               # загрузка зашифрованного файла
        save_file(encode(file, reverse_dictionary(load_dictionary())), "decoded.txt", False)                # загрузка таблицы Хаффмана, переворот это таблицы, расшифровка и сохранение расшифрованного файла

main()  # запуск основной функции
