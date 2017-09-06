# artificial-intelligence
These are the course projects of CSCI561 in University of Southern California. 
## Knowledge-Based Q&A System
Designed a knowledge-based Q&A system allowing users to tell acquired knowledge and ask new facts.
Used LEX and YACC to translate English sentences into CNF form of first-order logic. Designed tree-based index to improve the speed of search.
Had the ability to process over 1,000 sentences and the speed could be improved to less than 0.5s per query.
### Built With
* LEX & YACC - parse the input sentense and construct the grammar tree.
* Tree-based index.
* Python.
## Territory Game
Simulation of a territory game and has the following rules:
* The game board is an NxN grid representing the territory your	forces will	trample	(N=5 in the	figures	below).	Columns	are	named	A, B,	C,	…	starting from	the	left,	and	rows are named 1, 2, 3,	…	from top.
* Each	player	takes	turns	as	in	chess	or	tic-tac-toe.	That	is,	player	X	takes	a	move,	then	player	O,	then	back	to	player	X,	and	so	forth.	
* Each	square	has	a	fixed	point	value	between	1	and	99,	based	upon	its	computed	strategic	and	resource	value.
* The	object	of	the	game	for	each	player	is	to	score	the	most	points,	where	score	is	the	sum	of	all	point	values	of	all	his	or	her	occupied	squares	minus	the	sum	of	all	points	in	the	squares	occupied	by	the	other	player.	Thus,	one	wants	to	capture	the	squares	worth	the	most	points	while	preventing	the	other	player	to	do	so.
* The	game	ends	when	all	the	squares	are	occupied	by	the	players	since	no	more	moves	are	left.
* Players	cannot	pass	their	move,	i.e.,	they	must	make	a	valid	move	if	one	exists	(game	is	not	over).
* Movement	and	adjacency	relations	are	always	vertical	and	horizontal	but	never	diagonal.
* The	values	of	the	squares	can	be	changed	for	each	game,	but	remain	constant	within	a	game.
* Game	score	is	computed	as	the	difference	between	(a)	the	sum	of	the	values	of	all	squares	occupied	by	your	player	and	(b)	the	sum	of	the	values	of	all	squares	occupied	by	the	other	player.	This	applies	both	to	terminal	(game	over,	terminal	utility	function)	and	non-terminal	states	(evaluation	function).	This	is	required	to	ensure	that	your	program	produces	the	same	results	as	the	grading	script.
* On	each	turn,	a	player	can	make	one	of	two	moves:
### Built With
* **Minimax** game tree with **Alpha-Beta pruning**.
* Python version - simplisity in code.
* C++ version - better performance in running time.
## Los Angeles Travel Search
Given a list of freeway of road	intersections	(i.e., locations) and	the	time it would	take to	travel from	there	to other freeway or	road	intersections. Travel Search program will find the fastest route to	get	to destination. User can choose among four search algorithms - **breadth-first search**, **depth-first search**, **uniform-cost search** and **A\* search**	separately.
### Built With
* Python
* BFS, DFS, UCS, A\*
