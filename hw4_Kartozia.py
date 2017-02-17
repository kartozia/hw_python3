class Node:
    def __init__(self, data, next=None, position = 0):
        self.data = data
        self.next = next
        self.position = position


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def value_at(self, item): #вернуть значение узла в позиции index
        current = self.head
        while current != None:
            if current.data == item:
                return current.position
            else:
                current = current.next
        print ("item not present in list")

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
                node.position += 1               
            node.next = new_node
            
    def insert(self, data):
        new_node = Node(data, self.head)
        self.head = new_node

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.data() == data:
                found = True
            else:
                previous = current
                current = current.next
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.next
        else:
            previous = current.next
    
    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def value_n_from_end(self, n):
        current = self.head
        found = False
        index = self.size()
        need = index - n
        while current and found is False:
            if current.position == need:
                found = True
                return current
            else:
                current = current.next
        if current is None:
            raise ValueError("Data not in list")

    
n3 = Node(3)
n2 = Node(2, next=n3)
n1 = Node(1, next=n2)


l = LinkedList(head=n1)
for i in [1,2,3,4,5,4,5,6,6,6,6,1,1,54,3]:
    l.append(i)
l.printList()
