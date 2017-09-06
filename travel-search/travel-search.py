class minHeap(object):
	def __init__(self):
		self.heap = []
		self.dict = {}
		self.heapsize = 0
	def adjustdown(self, x):
		l = 2 * x + 1
		r = 2 * x + 2
		if l < self.heapsize and (self.heap[l][1] < self.heap[x][1] or (self.heap[l][1] == self.heap[x][1] and self.heap[l][2] < self.heap[x][2])):
			small = l
		else:
			small = x
		if r < self.heapsize and (self.heap[r][1] < self.heap[small][1] or (self.heap[r][1] == self.heap[small][1] and self.heap[r][2] < self.heap[small][2])):
			small = r
		if small != x:
			self.dict[self.heap[x][0]], self.dict[self.heap[small][0]] = self.dict[self.heap[small][0]], self.dict[self.heap[x][0]]
			self.heap[x], self.heap[small] = self.heap[small], self.heap[x]
			self.adjustdown(small)
	def insert(self, x, name, val, count):
		self.dict[name] = x
		if x >= len(self.heap):
			self.heap.append([name, val, count])
		else:
			self.heap[x] = [name, val, count]
		while x > 0 and (self.heap[(x - 1) / 2][1] > self.heap[x][1] or (self.heap[(x - 1) / 2][1] == self.heap[x][1] and self.heap[(x - 1) / 2][2] > self.heap[x][2])):
			self.dict[self.heap[x][0]], self.dict[self.heap[(x - 1) / 2][0]] = self.dict[self.heap[(x - 1) / 2][0]], self.dict[self.heap[x][0]]
			self.heap[x], self.heap[(x - 1) / 2] = self.heap[(x - 1) / 2], self.heap[x]
			x = (x - 1) / 2
	def find(self, name):
		if self.dict.get(name, None) == None:
			return -1
		else:
			return self.dict[name]

class Freeway(object):
	def __init__(self):
		#open file
		openfile = 'input.txt'
		f = open(openfile, 'r')
		#BFS or DFS or Uninformed or A*
		self.method = f.readline().strip()
		#start station
		self.start = f.readline().strip()
		#end station
		self.end = f.readline().strip()
		#number of livetraffic
		n = int(f.readline().strip())
		self.map = {}
		for i in range(n):
			path = f.readline().strip().split(' ')
			#add first station to map
			if self.map.get(path[0], None) == None:
				self.map[path[0]] = [[0, True]]
			#add second station to map
			if self.map.get(path[1], None) == None:
				self.map[path[1]] = [[0, True]]
			#add path to first station
			self.map[path[0]][0][0] += 1
			self.map[path[0]].append([path[1], int(path[2])])
		#number of the h function
		n = int(f.readline().strip())
		self.h = {}
		for i in range(n):
			path = f.readline().strip().split(' ')
			self.h[path[0]] = int(path[1])
		f.close()
	#bread-first search
	def BFS(self):
		from collections import deque
		#doulbe direction queue
		d = deque()
		#first is start station
		d.append(self.start)
		self.map[self.start][0][1] = False
		#travel root
		route = {}
		route[self.start] = -1
		while d:
			now = d.popleft()
			#find the end station
			if now == self.end:
				#generate reverse route
				ans = []
				while now != -1:
					ans.append(now)
					now = route[now]
				#prepare to write file
				count = 0
				writefile = 'output.txt'
				f = open(writefile, 'w')
				for i in range(len(ans) - 1, -1, -1):
					f.write(ans[i] + ' ' + str(count) + '\n')
					count += 1
				f.close()
				return
			for i in range(self.map[now][0][0]):
				#find next station
				next = self.map[now][i + 1][0]
				#check if it exist
				if self.map[next][0][1]:
					self.map[next][0][1] = False
					d.append(next)
					route[next] = now
	#depth-first search
	def DFS(self):
		stack = [self.start]
		route = {}
		route[self.start] = -1
		self.map[self.start][0][1] = False
		while stack:
			now = stack.pop()
			if now == self.end:
				#generate reverse route
				ans = []
				while now != -1:
					ans.append(now)
					now = route[now]
				#prepare to write file
				count = 0
				writefile = 'output.txt'
				f = open(writefile, 'w')
				for i in range(len(ans) - 1, -1, -1):
					f.write(ans[i] + ' ' + str(count) + '\n')
					count += 1
				f.close()
				return
			#search with the order
			for i in range(self.map[now][0][0] - 1, -1, -1):
				next = self.map[now][i + 1][0]
				#has not been search
				if self.map[next][0][1]:
					self.map[next][0][1] = False
					stack.append(next)
					route[next] = now
		
	def UCS(self):
		#use minimum heap to maintain the pirorityqueue
		h = minHeap()
		#initial minimum heap
		h.heapsize = 1
		count = 0
		h.insert(0, self.start, 0, count)
		route = {}
		route[self.start] = [-1, 0]
		while h.heapsize > 0:
			#use the min element
			[now, step, t] = h.heap[0]
			h.dict.pop(now)
			h.heap[0] = h.heap[h.heapsize - 1]
			h.heapsize -= 1
			if h.heapsize > 0:
				h.dict[h.heap[0][0]] = 0
				h.adjustdown(0)
			self.map[now][0][1] = False
			if now == self.end:
				#generate reverse route
				ans = []
				while now != -1:
					ans.append([now, route[now][1]])
					now = route[now][0]
				#prepare to write file
				writefile = 'output.txt'
				f = open(writefile, 'w')
				for i in range(len(ans) - 1, -1, -1):
					f.write(ans[i][0] + ' ' + str(ans[i][1]) + '\n')
				f.close()
				return
			for i in range(self.map[now][0][0]):
				[next, cost] = self.map[now][i + 1]
				#not search from next
				if self.map[next][0][1]:
					count += 1
					index = h.find(next)
					#not in the heap
					if index == -1:
						route[next] = [now, step + cost]
						h.heapsize += 1
						h.insert(h.heapsize - 1, next, step + cost, count)
					#exist in the heap and can renew
					elif step + cost < h.heap[index][1]:
						route[next] = [now, step + cost]
						h.insert(index, next, step + cost, count)
		
	def AStar(self):
		#use minimum heap to maintain the pirorityqueue
		h = minHeap()
		#initial minimum heap
		h.heapsize = 1
		count = 0
		h.insert(0, self.start, self.h[self.start], count)
		route = {}
		route[self.start] = [-1, 0]
		while h.heapsize > 0:
			#use the min element
			[now, step, t] = h.heap[0]
			step = route[now][1]
			h.dict.pop(now)
			h.heap[0] = h.heap[h.heapsize - 1]
			h.heapsize -= 1
			if h.heapsize > 0:
				h.dict[h.heap[0][0]] = 0
				h.adjustdown(0)
			self.map[now][0][1] = False
			if now == self.end:
				#generate reverse route
				ans = []
				while now != -1:
					ans.append([now, route[now][1]])
					now = route[now][0]
				#prepare to write file
				writefile = 'output.txt'
				f = open(writefile, 'w')
				for i in range(len(ans) - 1, -1, -1):
					f.write(ans[i][0] + ' ' + str(ans[i][1]) + '\n')
				f.close()
				return
			for i in range(self.map[now][0][0]):
				[next, cost] = self.map[now][i + 1]
				#not search from next
				if self.map[next][0][1] or (step + cost < route[next][1]):
					count += 1
					index = h.find(next)
					#not in the heap
					if index == -1:
						route[next] = [now, step + cost]
						h.heapsize += 1
						h.insert(h.heapsize - 1, next, step + cost + self.h[next], count)
					#exist in the heap and can renew
					elif step + cost + self.h[next]< h.heap[index][1]:
						route[next] = [now, step + cost]
						h.insert(index, next, step + cost + self.h[next], count)
				
	def SearchPath(self):
		#start and end is same
		if self.start == self.end:
			writefile = 'output.txt'
			f = open(writefile, 'w')
			f.write(self.start + ' 0' + '\n')
			f.close()
			return
			
		way = {'BFS':self.BFS, 'DFS':self.DFS, 'UCS':self.UCS, 'A*':self.AStar}
		way[self.method]()
		
import pdb
#pdb.set_trace()
a = Freeway()
a.SearchPath()
