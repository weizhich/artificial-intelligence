class Game(object):
	def __init__(self):
		#open file
		openfile = 'input.txt'
		f = open(openfile, 'r')
		#dimension of the board
		self.n = int(f.readline().strip())
		#search method
		self.method = f.readline().strip()
		#which chess I should play
		self.my = f.readline().strip()
		self.op = 'O' if self.my == 'X' else 'X'
		#the depth of search
		self.depth = int(f.readline().strip())
		#initial board values
		self.value = [[] for i in range(self.n)]
		for i in range(self.n):
			rowValue = f.readline().strip().split(' ')
			for element in rowValue:
				self.value[i].append(int(element))
		#initial board and score
		self.score = 0
		self.ininumber = 0
		self.board = [[] for i in range(self.n)]
		for i in range(self.n):
			rowPiece = f.readline().strip()
			for j in range(self.n):
				c = rowPiece[j]
				self.board[i].append(c)
				if c == self.my:
					self.score += self.value[i][j]
					self.ininumber += 1
				elif c == self.op:
					self.score -= self.value[i][j]
					self.ininumber += 1
		f.close()
	
	def MiniMaxDecision(self):
		return self.MaxValue(self.ininumber, 1)
	def AlphaBetaSearch(self):
		return self.MaxValueAlphaBeta(self.ininumber, 1, -2147483648, 2147483647)
		
	def MaxValue(self, number, depth):
		if number == self.n * self.n or depth == self.depth + 1:
			return self.score
		v = -2147483648
		raidset = []
		for i in range(self.n):
			for j in range(self.n):
				if self.board[i][j] != '.':
					continue
				hash = self.checkAdjecent(i, j)
				self.board[i][j] = self.my
				self.score += self.value[i][j]
				#move type is Raid then add it to the set
				if hash.get(self.my, None) != None and hash.get(self.op, None) != None:
					raidset.append((i, j))
				nextv = self.MinValue(number + 1, depth + 1)
				if nextv > v:
					v = nextv
					x = i
					y = j
					type = 'Stake'
				self.board[i][j] = '.'
				self.score -= self.value[i][j]
		#check all Raid moves
		for (i, j) in raidset:
			hash = self.checkAdjecent(i, j)
			self.board[i][j] = self.my
			self.score += self.value[i][j]
			for (xx, yy) in hash[self.op]:
				self.board[xx][yy] = self.my
				self.score += 2 * self.value[xx][yy]
			nextv = self.MinValue(number + 1, depth + 1)
			if nextv > v:
				v = nextv
				x = i
				y = j
				type = 'Raid'
			for (xx, yy) in hash[self.op]:
				self.board[xx][yy] = self.op
				self.score -= 2 * self.value[xx][yy]
			self.board[i][j] = '.'
			self.score -= self.value[i][j]
		if depth == 1:
			return ((x, y), type)
		else:
			return v
	
	def MinValue(self, number, depth):
		if number == self.n * self.n or depth == self.depth + 1:
			return self.score
		v = 2147483647
		raidset = []
		for i in range(self.n):
			for j in range(self.n):
				if self.board[i][j] != '.':
					continue
				hash = self.checkAdjecent(i, j)
				self.board[i][j] = self.op
				self.score -= self.value[i][j]
				if hash.get(self.op, None) != None and hash.get(self.my, None) != None:
					raidset.append((i, j))
				v = min(v, self.MaxValue(number + 1, depth + 1))
				self.board[i][j] = '.'
				self.score += self.value[i][j]
		for (i, j) in raidset:
			hash = self.checkAdjecent(i, j)
			self.board[i][j] = self.op
			self.score -= self.value[i][j]
			for (xx, yy) in hash[self.my]:
				self.board[xx][yy] = self.op
				self.score -= 2 * self.value[xx][yy]
			v = min(v, self.MaxValue(number + 1, depth + 1))
			for (xx, yy) in hash[self.my]:
				self.board[xx][yy] = self.my
				self.score += 2 * self.value[xx][yy]
			self.board[i][j] = '.'
			self.score += self.value[i][j]
		return v
	
	def MaxValueAlphaBeta(self, number, depth, alpha, beta):
		if number == self.n * self.n or depth == self.depth + 1:
			return self.score
		v = -2147483648
		raidset = []
		for i in range(self.n):
			for j in range(self.n):
				if self.board[i][j] != '.':
					continue
				hash = self.checkAdjecent(i, j)
				self.board[i][j] = self.my
				self.score += self.value[i][j]
				#move type is Raid then add it to the set
				if hash.get(self.my, None) != None and hash.get(self.op, None) != None:
					raidset.append((i, j))
				nextv = self.MinValueAlphaBeta(number + 1, depth + 1, alpha, beta)
				if nextv > v:
					v = nextv
					x = i
					y = j
					type = 'Stake'
				self.board[i][j] = '.'
				self.score -= self.value[i][j]
				if v >= beta:
					return v
				alpha = max(alpha, v)
		#check all Raid moves
		for (i, j) in raidset:
			hash = self.checkAdjecent(i, j)
			self.board[i][j] = self.my
			self.score += self.value[i][j]
			for (xx, yy) in hash[self.op]:
				self.board[xx][yy] = self.my
				self.score += 2 * self.value[xx][yy]
			nextv = self.MinValueAlphaBeta(number + 1, depth + 1, alpha, beta)
			if nextv > v:
				v = nextv
				x = i
				y = j
				type = 'Raid'
			for (xx, yy) in hash[self.op]:
				self.board[xx][yy] = self.op
				self.score -= 2 * self.value[xx][yy]
			self.board[i][j] = '.'
			self.score -= self.value[i][j]
			if v >= beta:
				return v
			alpha = max(alpha, v)
		if depth == 1:
			return ((x, y), type)
		else:
			return v
			
	def MinValueAlphaBeta(self, number, depth, alpha, beta):
		if number == self.n * self.n or depth == self.depth + 1:
			return self.score
		v = 2147483647
		raidset = []
		for i in range(self.n):
			for j in range(self.n):
				if self.board[i][j] != '.':
					continue
				hash = self.checkAdjecent(i, j)
				self.board[i][j] = self.op
				self.score -= self.value[i][j]
				if hash.get(self.op, None) != None and hash.get(self.my, None) != None:
					raidset.append((i, j))
				v = min(v, self.MaxValueAlphaBeta(number + 1, depth + 1, alpha, beta))
				self.board[i][j] = '.'
				self.score += self.value[i][j]
				if v <= alpha:
					return v
				beta = min(beta, v)
		for (i, j) in raidset:
			hash = self.checkAdjecent(i, j)
			self.board[i][j] = self.op
			self.score -= self.value[i][j]
			for (xx, yy) in hash[self.my]:
				self.board[xx][yy] = self.op
				self.score -= 2 * self.value[xx][yy]
			v = min(v, self.MaxValueAlphaBeta(number + 1, depth + 1, alpha, beta))
			for (xx, yy) in hash[self.my]:
				self.board[xx][yy] = self.my
				self.score += 2 * self.value[xx][yy]
			self.board[i][j] = '.'
			self.score += self.value[i][j]
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v
		
	def checkAdjecent(self, x, y):
		hash = {}
		dir = [[-1, 0], [1, 0], [0, 1], [0, -1]]
		for i in range(4):
			xx = x + dir[i][0]
			yy = y + dir[i][1]
			if xx >= 0 and xx < self.n and yy >= 0 and yy < self.n and self.board[xx][yy] != '.':
				next = self.board[xx][yy]
				if hash.get(next, None) == None:
					hash[next] = [(xx, yy)]
				else:
					hash[next].append((xx, yy))
		return hash
		
	
	
	def play(self):
		way = {'MINIMAX':self.MiniMaxDecision, 'ALPHABETA':self.AlphaBetaSearch}
		((x, y), type) = way[self.method]()
		self.board[x][y] = self.my
		hash = self.checkAdjecent(x, y)
		if type == 'Raid' and hash.get(self.op, None) != None:
			for (xx, yy) in hash[self.op]:
				self.board[xx][yy] = self.my
		writefile = 'output.txt'
		f = open(writefile, 'w')
		f.write(chr(y + 65) + str(x + 1) + ' ' + type + '\n')
		for i in range(self.n):
			f.write(''.join(self.board[i]) + '\n')
		f.close()

import time
start = time.clock()
test = Game()
test.play()
end = time.clock()
print "running time: %f s" % (end -start)
"""
print test.my
print test.op
print test.n
print test.depth
print test.method
print test.value
print test.board
print test.score
"""