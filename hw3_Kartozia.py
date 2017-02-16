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

     def pop(self): 
          return self.items.pop()

     def peek(self):
         element = self.items[len(self.items)-1]
         return self.items[element]

class MyQueue(Stack):
     def __init__(self):
         self.first = Stack()
         self.second = Stack()
         
     def make_stack(self, item):
          self.first.push(item)

     def reverse_stack(self):
          if not self.first.isEmpty():
               while len(self.first.items) > 0:
                    self.second.push(self.first.pop())
               queue = self.second.pop()
               while len(self.second.items)> 0:
                    self.first.push(self.second.pop())
               return queue
          
q = MyQueue()
for i in range(10):
     q.make_stack(i)
for i in range(10):
     print (q.reverse_stack())
