import unittest

def to_table(list1, key, list2):
    """ красиво оформляет результат в виде таблицы keyword in context
    list1 — массив слов слева от ключевого слова
    key — ключевое слово
    list2 — массив слов справа от ключевого слова
    Внутри функции элементы массивов объединятся в строку, создавая сниппет
    """
    str1 = ' '.join(list1)
    str2 = ' '.join(list2)
    return str1 + '\t' + key + '\t' + str2 + '\n'

def kwiq(word, text, num=3):
    """Принимает на вход слово и текст, а возвращает сниппеты с этим словом из текста
    word — слово, которое функция ищ в тексте
    text — текст, в котором ищется заданое пользователем слово
    num — задает количество слов в сниппете вокруг искомого слова, по умолчанию равно 3
    Из текста создаётся массив слов, в котором ищется заданое слово.
    Потом функция ищет контекст, заданной длины, слева и справа от слово.
    В результате функция возвращает сниппет в формате keyword in context
    """
    #[item for item in range(len(words)) if words[item] == word]
    snippets = []
    arr = text.split()
    index = [w for w in range(len(arr)) if arr[w] == word]
    for i in index:
        key_word = arr[i]
        num_end = num + 1
        start = i+ num
        end = i + num_end
        left = arr[start:start+num]
        right = arr[end-num:end]
        snippets.append(to_table(left, key_word, right))
    for s in snippets:
        print(s)
        
##    return snippets

file = open('contrl.txt', 'r', encoding='utf-8')
test = file.read()
print(kwiq('контрольная', test, 3))
