from queue import PriorityQueue
import pickle

class Node:                         # создание класса для постояния бинарного дерева
    def __init__(self) -> None:     # создание конструктора класса, вызываемого при создании узла бинарного дерева
        self.symbol = None          # создание переменой, равной None, если не является конечной вершиной
        self.left = None
        self.right = None

    def __lt__(self, other):        # переопределение оператора "больше", необходимого для работы приоритетной очереди
        return True                 # всегда возвращает True (может вызывать ошибки)
    
def scan(node, code, dictionary):   # рекурсивная функция поиска в глубину
    if node.symbol == None:
        scan(node.left, code + "1", dictionary)
        scan(node.right, code + "0", dictionary)
    else:
        code = '1' + code
        if node.symbol == '\n':
            print("\'\\n\': ", code, " (", int(code, 2), ")", sep='')
        else:
            print("\'", node.symbol, "\' : ", code, " (", int(code, 2), ")", sep='')
        dictionary[node.symbol] = code
    return dictionary

def generate_dictionary(file):
    symbols = {}
    for symbol in file:
        if symbols.get(symbol) == None:
            symbols[symbol] = 1
        else:
            symbols[symbol] += 1

    queue = PriorityQueue()
    for k in symbols:
        temp = Node()
        temp.symbol = k
        queue.put((symbols.get(k), temp))

    while queue.qsize() != 1:
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

def read_file(name, is_encodeed):   # функция чтения файла
    if is_encodeed:
        link_code_txt = open(name, "rb")
        temp = link_code_txt.read()
        link_code_txt.close()
        return temp
    else:        
        link_code_txt = open(name, "rt", encoding="utf-8-sig")
        file = ''
        for str_temp in link_code_txt:
            for char_temp in str_temp:
                file += char_temp
        link_code_txt.close()
        return file
    
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def encode(file, dictionary):   # функция шифрования
    decoded_file = ""
    for temp in file:
        decoded_file += dictionary.get(temp)
    return bitstring_to_bytes(decoded_file)

def decode(file, dictionary):   # функция расшифрования
    temp = ''
    c = ''
    decoded_file = ''
    temp = bin(file[0])[2:]
    for i in range(1, len(file)):
        temp += bin(file[i])[2:].zfill(8)
    for i in temp:
        c += i
        if dictionary.get(c) != None:
            decoded_file += dictionary[c]
            c = ''
    return decoded_file

def reverse_dictionary(dictionary): # функция разворота таблицы Хаффмана
    reverse_dictionary = {}
    print(dictionary)
    for temp in dictionary:
        reverse_dictionary[dictionary[temp]] = temp
    return reverse_dictionary

def save_file(file, name, is_encoded):  # функция сохранения файла
    try:
        if is_encoded:
            f = open(name, "wb")
            f.write(file)
        else:
            f = open(name, "w")
            f.write(file)
    finally:
        f.close()

def save_dictionary(dictionary):    # функция сохранения словаря
    pickle.dump(dictionary, open("haffman_dictionary.txt", 'wb'))

def load_dictionary():              # функция загрузки словаря
    return pickle.load(open("haffman_dictionary.txt", 'rb'))

def main():     # объявление основной функции
        mode = int(input("Для шифрования файла введите 0\nДля расшифрования файла введите 1\nВыбор режима: "))
        if mode == 0:
            file = read_file("code.txt", False)
            dictionary = generate_dictionary(file)
            save_dictionary(dictionary)
            save_file(encode(file, dictionary), "encoded.bin", True)
        elif mode == 1:
            file = read_file("encoded.bin", True)
            print(reverse_dictionary(load_dictionary()))
            save_file(decode(file, reverse_dictionary(load_dictionary())), "decoded.txt", False)
            
if __name__ == "__main__":
    main()  # запуск основной функции