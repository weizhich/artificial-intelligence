temp = '((#P(bob))()'
literal = temp.split('|')
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
	print predicate
	print negative
	print para_list
	print '--------------------'