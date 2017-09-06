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
	
y = ['x1', 'y1']
x = ['Tom', 'y2']
import pdb
print unify_two_list(x, y)