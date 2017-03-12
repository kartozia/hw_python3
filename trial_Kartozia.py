#Тренировочная работа, Картозия (голландский прокрастинатор),БКЛ141

from collections import Counter
import itertools

#задание №1
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

#задание №2
def main_counter(text): # подсчёт кол-ва идиом, где встречается основное слово
    arr = []
    for line in text:
        line = line.split()
        main_word = line[1].strip()
        arr.append(main_word)
        main_occurences = Counter(arr)     
    return main_occurences #вернет все идиомы
    #return main_occurences.most_common([50]) #возвращает 50 самых частотных
# не понятно, почему most_common не работает:    if n >= size:
#TypeError: unorderable types: list() >= int()

def attribute_counter(text): # подсчёт кол-ва идиом, где встречается основное слово
    arr = []
    for line in text:
        line = line.split()
        main_word = line[0].strip()
        arr.append(main_word)
        main_occurences = Counter(arr)     
    return main_occurences #вернет все идиомы       
    #return main_occurences.most_common([50]) #возвращает 50 самых частотных
print(attribute_counter(read_file('idioms_high')))

    
                             

