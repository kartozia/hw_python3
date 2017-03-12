from collections import Counter
import itertools

def read_file(text): #открывает файл и читает его построчно
    file = open(text +'.txt', 'r', encoding='utf-8')
    text = file.readlines()
    file.close()
    return text

def list_comprehension(text): #создает массив идиом
    idioms = read_file(text)
    arr = [i.strip() for i in idioms]
    return arr

def set_comprehension(text): #создает множество идиом
    idioms = read_file(text)
    arr = {i.strip() for i in idioms}
    return arr

idi = set_comprehension('idioms_high')
print(idi)
