# место для библиотек и отдельных функций из них
from queue import PriorityQueue 
import pickle

dictionary = {}

class Node:
    def __init__(self) -> None:
        self.symbol = None
        self.priority = 0
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return True

def scan(node, code):
    if node.symbol ==  None :
        scan(node.left, code + "1")
        scan(node.right, code + "0")
    else :
        #node.symbol
        print("\'", node.symbol, "\' : ", code[::-1], " ", int(code[::-1], 2), sep='')
        dictionary[node.symbol] = int(code[::-1], 2)


def copy_message():                                                 # функция построчного копирования 
    str_codes = []
    link_code_txt = open("code.txt", "rt", encoding = "utf-8-sig")  # открытие файла на чтение в текстовом режиме с текстом на русском или английском языке
    for str_code in link_code_txt:
        print(str_code, end = '')
        str_codes.append(str_code)
    link_code_txt.close()
    return str_codes                                                # возвращаемое значение

def main():                     # основная функция
    str_code = copy_message()
    symbols = {} 
    for string in str_code :
        for symbol in string :
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
    
    temp = queue.get() #TODO если файл сосотоит из 1 символа, выкинуть ошибку
    scan(temp[1], "")
    table = pickle.dumps(dictionary)
    print(table)
    table2 = pickle.loads(table)
    print(table2)

main()
