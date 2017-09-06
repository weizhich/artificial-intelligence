s1 = 'A(x)'
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
print oper1