class Node:
	def __init__(self, data, prev=None, next=None):
		self.data = data
		self.prev = prev
		self.next = next

class List:
	def __init__(self):
		self.head = Node(None)
		self.tail = Node(None, self.head)
		self.head.next = self.tail
		self.size = 0
	
	def listSize(self):
		return self.size
	
	def seekNode(self, index):
		if self.size/2 > index :

		else :
			
	
