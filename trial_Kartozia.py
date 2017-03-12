#Тренировочная работа, Картозия (голландский прокрастинатор),БКЛ141

from collections import Counter
import itertools

#задание №1
def read_file(name): #открывает файл и читает его построчно
    file = open(name +'.txt', 'r', encoding='utf-8')
    text = file.readlines()
    file.close()
    return text

def create_file(name): #создаёт файл для записи и возвращает его
    file = open(name +'.txt', 'w', encoding='utf-8')
    return file

def list_comprehension(text): #создает массив идиом
    idioms = read_file(text)
    arr = [i.strip() for i in idioms]
    return arr

def set_comprehension(text): #создает множество идиом
    idioms = read_file(text)
    arr = {i.strip() for i in idioms}
    return arr

#задание №2
def main_list(name): #создаёт список основных слов
    text = read_file(name)
    arr = []
    for line in text:
        line = line.split()
        main_word = line[1].strip()
        arr.append(main_word)
    return arr

def attribute_list(name): #создаёт список аттрибутов
    text = read_file(name)
    arr = []
    for line in text:
        line = line.split()
        att_word = line[0].strip()
        arr.append(att_word)
    return arr
    
def main_counter(arr): # подсчёт кол-ва идиом, где встречается основное слово
    main_occurences = Counter(arr)     
    return main_occurences #вернет все идиомы
    #return main_occurences.most_common([50]) #возвращает 50 самых частотных
# не понятно, почему most_common не работает:    if n >= size:
#TypeError: unorderable types: list() >= int()

def attribute_counter(arr): # подсчёт кол-ва идиом, где встречается основное слово
    att_occurences = Counter(arr)     
    return att_occurences #вернет все идиомы       
    #return att_occurences.most_common([50]) #возвращает 50 самых частотных

# задание №3a
def generate_pairs(main, att): #генерирует все возможные пары, файл который я создавала,
                              #чтобы посмотреть,что выходит, не открывается из-за insufficent memory
                            # itertools.islice(pairs,10), но часть можно увидеть через islice
    pairs = itertools.product(att, main)
    for i in pairs:
        i = ' '.join(i)
    return pairs

def new_pairs(main, att, text): 
    existing_pairs = list_comprehension(text)
    all_pairs = generate_pairs(main, att)
    new = list(itertools.filterfalse(existing_pairs, all_pairs))
    file = create_file('all_pairs')
    for n in new:
        file.write(n+'\n')
    file.close()
    return '3a complete'

print(new_pairs(main_list('idioms_high'), attribute_list('idioms_high'), 'idioms_high'))


    
                             

