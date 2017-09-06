tokens = (
	'PREDICATE',
	'NEGPREDICATE',
	'NOT',
	'AND',
	'OR',
	'LPAREN',
	'RPAREN',
	'IMPLY',
)
# Tokens
t_PREDICATE = r'[A-Z_][a-zA-Z_]*[(][a-zA-Z,_]*[)]'
t_NEGPREDICATE = r'[#][A-Z_][a-zA-Z_]*[(][a-zA-Z,_]*[)]'
t_NOT = r'\~'
t_AND = r'\&'
t_OR = r'\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IMPLY = r'\=>'
	
t_ignore = " \t"
	
def t_newline(t):
	r'\n+'
	t.lineno += t.value.count("\n")
	
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
# Build the lexer
import ply.lex as lex
lexer = lex.lex()
	

# Parsing rules
precedence = (
	('left','IMPLY'),
	('left','AND','OR'),
	('right','NOT'),
	)

def p_statment_expression(t):
	'statement : expression'
	global temp
	temp = t[1][ : ]
	
def p_expression_imple(t):
	'expression : expression IMPLY sentense'
	t[0] = ''
	flag = True
	for ch in t[1]:
		if ch in ['(',  ')', ',']:
			t[0] += ch
		elif ch == '&':
			t[0] += '|'
			flag = True
		elif ch == '|':
			t[0] += '&'
			flag = True
		elif ch == '#':
			flag = False
		elif flag:
			t[0] += '#' + ch
			flag = False
		else:
			t[0] += ch
	t[0] += '|' + t[3]

def p_expression_sentense(t):
	'expression : sentense'
	t[0] = t[1]

def p_sentense_and(t):
	'sentense : sentense AND term'
	t[0] = t[1] + t[2] + t[3]

def p_sentense_or(t):
	'sentense : sentense OR term'
	t[0] = t[1] + t[2] + t[3]
	def distributer(a, b):
		list1 = a.split('&')
		list2 = b.split('&')
		ans = ''
		for s1 in list1:
			oper1 = ''
			flag = False
			for ch in s1:
				if ch == '|':
					oper1 += ch
				elif ch not in ['(', ')']:
					flag = True
					oper1 += ch
				elif ch == '(' and flag:
					oper1 += ch
				elif ch == ')' and flag:
					oper1 += ch
					flag = False
			for s2 in list2:
				oper2 = ''
				flag = False
				for ch in s2:
					if ch == '|':
						oper2 += ch
					elif ch not in ['(', ')']:
						flag = True
						oper2 += ch
					elif ch == '(' and flag:
						oper2 += ch
					elif ch == ')' and flag:
						oper2 += ch
						flag = False
				ans += '(' + oper1 + '|' + oper2 + ')' + '&'
		return ans[ : -1]
	if distribution:
		t[0] = distributer(t[1], t[3])
def p_sentense_term(t):
	'sentense : term'
	t[0] = t[1]

def p_term_not(t):
	'term : NOT factor'
	t[0] = ''
	flag = True
	for ch in t[2]:
		if ch in ['(',  ')', ',']:
			t[0] += ch
		elif ch == '&':
			t[0] += '|'
			flag = True
		elif ch == '|':
			t[0] += '&'
			flag = True
		elif ch == '#':
			flag = False
		elif flag:
			t[0] += '#' + ch
			flag = False
		else:
			t[0] += ch


def p_term_factor(t):
	'term : factor'
	t[0] = t[1]

def p_factor_predict(t):
	'factor : PREDICATE'
	t[0] = t[1]
	
def p_factor_negpredict(t):
	'factor : NEGPREDICATE'
	t[0] = t[1]
	
def p_factor_expression(t):
	'factor : LPAREN expression RPAREN'
	t[0] = t[1] + t[2] + t[3]
	
def p_error(t):
	print("Syntax error at '%s'" % t.value)

def add_CNF_KB(sen, kb_pre, temp, no):
	literal = temp.split('|')
	sen[no] = [0]
	length = 0
	for pre in literal:
		flag = 0
		negative = False
		predicate = ''
		paramaters = ''
		for ch in pre:
			if ch == '(' and flag == 0:
				pass
			elif ch == '(' and flag == 1:
				flag = 2
			elif ch == ')':
				break
			elif ch == '#':
				flag = 1
				negative = True
			elif flag == 0:
				flag = 1
				predicate += ch
			elif flag == 1:
				predicate += ch
			elif flag == 2:
				paramaters += ch
		para_list = paramaters.split(',')
		#standarize variables
		for i in range(len(para_list)):
			if ord(para_list[i][0]) > 96:
				para_list[i] += str(no)
		length += 1
		sen[no].append((predicate, not negative, para_list))
		if kb_pre.get(predicate, None) == None:
			kb_pre[predicate] = [(no, length, not negative, para_list)]
		else:
			kb_pre[predicate].append((no, length, not negative, para_list))
	sen[no][0] = length

def unify_two_list(x, y):
	theta = {}
	i, length = 0, len(x)
	while i < length:
		a, b = x[i], y[i]
		if a == b:
			i += 1
			continue
		#varable a
		elif ord(a[0]) > 96:
			if theta.get(a, None) != None:
				x[i] = theta[a]
			elif theta.get(b, None) != None:
				y[i] = theta[b]
			else:
				i += 1
				theta[a] = b
			
		elif ord(b[0]) > 96:
			if theta.get(a, None) != None:
				x[i] = theta[a]
			elif theta.get(b, None) != None:
				y[i] = theta[b]
			else:
				i += 1
				theta[b] = a
		else:
			return 'failure'
	theta1 = {}
	for key, p in theta.items():
		while theta.get(p, None) != None:
			p = theta[p]
		theta1[key] = p
	return theta1
	
def get_str(tup):
	ans = tup[0]
	if tup[1]:
		ans += '1'
	else:
		ans += '0'
	count = 0
	for ele in tup[2]:
		if ord(ele[0]) > 96:
			count += 1
			ans += 'x' + str(count)
		else:
			ans += ele
	return ans

def kb_ask(KB_sen, KB_pre, tup, ind):
	from collections import deque
	import pdb
	import time
	start = time.clock()
	#add the negation to the KB
	KB_sen[ind] = [1]
	KB_sen[ind].append((tup))
	if KB_pre.get(tup[0], None) == None:
		return False
	KB_pre[tup[0]].append((ind, 1, tup[1], tup[2]))
	#pdb.set_trace()
	occur_check = set()
	support_set = deque()
	support_set.append([tup])
	no = 0
	count = 0
	while support_set:
		end = time.clock()
		if (end - start >= 29):
			return False
		now_list = support_set.popleft()
		str_ele = ''
		for ele in now_list:
			str_ele += get_str(ele)
		if str_ele in occur_check:
			continue
		else:
			occur_check.add(str_ele)
		'''
		count += 1
		if count == 3:
			pdb.set_trace()
		'''
		length = len(now_list)
		for k in range(1):
			ele = now_list[k]
			if KB_pre.get(ele[0], None) == None:
				continue
			for check_ele in KB_pre[ele[0]]:
				#has the same truth value
				if check_ele[2] == ele[1]:
					'''
					if length == 1 and check_ele[0] != ind and KB_sen[check_ele[0]][0] == 1 and unify_two_list(check_ele[3], ele[2]) != 'failure':
						#remove negation from kb
						KB_pre[tup[0]].pop()
						return False
					'''
					pass
				else:
					theta = unify_two_list(check_ele[3], ele[2])
					if theta == 'failure':
						continue 
					no += 1
					add_list = []
					#add the rest of KB sentense
					for i in range(1, KB_sen[check_ele[0]][0] + 1):
						if i == check_ele[1]:
							continue
						temp_tup = KB_sen[check_ele[0]][i]
						temp_para = []
						for para in temp_tup[2]:
							if theta.get(para, None) != None:
								key = theta[para]
							else:
								key = para
							if ord(key[0]) > 96:
								key += '#' + str(no)
							temp_para.append(key)
						add_list.append((temp_tup[0], temp_tup[1], temp_para))
					#add the rest of support_set sentense
					for i in range(length):
						if i == k:
							continue
						temp_tup = now_list[i]
						temp_para = []
						for para in temp_tup[2]:
							if theta.get(para, None) != None:
								key = theta[para]
							else:
								key = para
							if ord(key[0]) > 96:
								key += '#' + str(no)
							temp_para.append(key)
						add_list.append((temp_tup[0], temp_tup[1], temp_para))
					if not add_list:
						#remove negation from kb
						KB_pre[tup[0]].pop()
						return True
					else:
						'''
						print add_list
						print '________________________'
						'''
						support_set.append(add_list)
	#remove negation from kb
	KB_pre[tup[0]].pop()
	return False

#initial yacc parse
import ply.yacc as yacc
yacc.yacc()
#initial read input
#open file
openfile = 'input.txt'
#import time
#start = time.clock()
f = open(openfile, 'r')
#number of query
n = int(f.readline().strip())
query_list = []
for i in range(n):
	temp_s = ''.join(f.readline().strip().split(' '))
	flag = 0
	predicate = ''
	paramaters = ''
	negative = False
	for ch in temp_s:
		if ch == '~':
			negative = True
		elif ch == '(':
			flag = 1
		elif ch == ')':
			pass
		elif flag == 0:
			predicate += ch
		elif flag == 1:
			paramaters += ch
	query_list.append((predicate, negative, paramaters.split(',')))
#initial build the kernel base
n = int(f.readline().strip())
global temp
global distribution
#initial a empty KB using predicate table
KB_sen = {}
KB_pre = {}
number = 0
for i in range(n):
	input_str = f.readline().strip().split(' ')
	temp = ''
	distribution = False
	#imply elimination and move negation inward
	yacc.parse(''.join(input_str))
	# distribute | over &
	distribution = True
	yacc.parse(temp)
	#add CNF to KB
	clause_list = temp.split('&')
	for clause in clause_list:
		number += 1
		add_CNF_KB(KB_sen, KB_pre, clause, number)
#close the input file 
f.close()
#show my KB
'''
print KB_sen
print '--------------'
print KB_pre
'''
#prepare to query 
#open the output file
writefile = 'output.txt'
f = open(writefile, 'w')
for tup in query_list:
	#query and write to the output file
	if kb_ask(KB_sen, KB_pre, tup, number + 1):
		f.write('TRUE\n')
	else:
		f.write('FALSE\n')
f.close()
#end = time.clock()
#print end - start


