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
        string = to_table(left, key_word, right)
        snippets.append(string)
    return snippets

file = open('contrl.txt', 'r', encoding='utf-8')
ctrl = file.read()

class SnippetTest(unittest.TestCase):
    """ Класс тестирует функцию kwiq
    Запускаем функцию внутри класса и проверяем, правильной ли длины выдаётся нам сниппет
    при помощи функции test_len.
    Например, если мы задаём num=3 (по три слова по обе стороны от ключевого слова), то
    длина сниппета будет 3+3+1, где один это ключевое слово. Общий вид: num*2+1
    """
    def test_len(self, word, text, num=3):
        for i in kwiq(word,text, num):
            self.assertEqual(len(i.split()), num*2+1)

test = SnippetTest()
print(test.test_len('контрольная', ctrl, 5))
        
#print(kwiq('контрольная', ctrl))
