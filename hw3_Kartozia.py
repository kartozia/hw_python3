class Stack:
     def __init__(self):
          self.items = []

     def isEmpty(self):
          if self.items == []:
               return True
          else:
               return False

     def push(self, item):
          self.items.append(item)

     def pop(self):  # удалить элемент из стека и вернуть его значение
          element = self.items.pop()
          return self.items[element]

     def peek(self):
         element = self.items[len(self.items)-1]
         return self.items[element]

class MyQueue(Stack):
    def __init__(self):
         self.que = []
         first = Stack()
         second = Stack()

     def make_queue(self, item):
          first.push(item)
          for i in first.items:
               second.push(i)
          self.que = second.items
          return self.que


    
