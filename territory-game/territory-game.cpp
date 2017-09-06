#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <limits.h>

using namespace std;

class Game{
private:
	char my;					//my piece
	char op;					//oppoent piece
	int n;						//the deminsion of board
	int depth;					//search depth
	char board[26][26];			//board
	int value[26][26];			//the value on each square
	char method;				//the method of search
	int score;					//my score
	int number;					//total number on the board
	char type;					//type of movement
	int ansX, ansY;				//the position we choose
	int way[4][2];
public:
	Game();						//construct function
	void Search();				//search function
	void Print();
	int MaxValue(int number, int depth);//MaxValue
	int MinValue(int number, int depth);//MinValue
	int MaxValueAlphaBeta(int number, int depth, int alpha, int beta);
	int MinValueAlphaBeta(int number, int depth, int alpha, int beta);
	bool CheckRaid(int x, int y, bool* move, char mypiece);
};
Game::Game(){					//construct method
	ifstream fin("input.txt");	//open input.txt
	this->way[0][0] = -1; this->way[0][1] = 0;
	this->way[1][0] = 1; this->way[1][1] = 0;
	this->way[2][0] = 0; this->way[2][1] = -1;
	this->way[3][0] = 0; this->way[3][1] = 1;
	this->score = 0; this->number = 0;
	string s;
	getline(fin, s);
	this->n = atoi(s.c_str());	//read n
	getline(fin, s);
	this->method = s[0];		//read method
	getline(fin, s);			//read my piece
	this->my = s[0];
	if (this->my == 'X')
		this->op = 'O';
	else
		this->op = 'X';			//determine oppoent piece
	getline(fin, s);
	this->depth = atoi(s.c_str());	//read depth
	for (int i = 0; i < this->n; i++){
		getline(fin, s);
		char* c;
		const int len = s.length();
		c = new char[len + 1];
		strcpy(c, s.c_str());
		const char* split = " ";
		char* p = NULL;
		p = strtok(c, split);
		for (int j = 0; j < this->n; j++){
			this->value[i][j] = atoi(p);
			p = strtok(NULL, split);
		}
	}

	for (int i = 0; i < this->n; i++){
		getline(fin, s);
		strcpy(this->board[i], s.c_str());
		for (int j = 0; j < this->n; j++){
			if (s[j] == this->my){
				this->score += this->value[i][j];
				this->number++;
			}
			if (s[j] == this->op){
				this->score -= this->value[i][j];
				this->number++;
			}
		}
	}
	fin.close();
}
void Game::Search(){
	if (this->method == 'M')
		this->MaxValue(this->number, 1);
	else
		this->MaxValueAlphaBeta(this->number, 1, INT_MIN, INT_MAX);
}
void Game::Print(){
	ofstream file("output.txt");
	file << char(this->ansY + 65) << this->ansX + 1 << ' ';
	if (this->type == 'R')
		file << "Raid\n";
	else
		file << "Stake\n";
	this->board[this->ansX][this->ansY] = this->my;
	if (this->type == 'R'){
		bool s[4];
		if (this->CheckRaid(this->ansX, this->ansY, s, this->my)){
			for (int k = 0; k < 4; k++){
				if (s[k])
					this->board[this->ansX + this->way[k][0]][this->ansY + this->way[k][1]] = this->my;
			}
		}
	}
	for (int i = 0; i < this->n; i++){
		for (int j = 0; j < this->n; j++)
			file << this->board[i][j];
		file << "\n";
	}
	file.close();
}
int Game::MaxValue(int number, int depth){
	if (number == this->n * this->n || depth == this->depth + 1)
		return this->score;
	int v = INT_MIN;
	char nowType;
	int nowX, nowY, nextv;
	for (int i = 0; i < this->n; i++){
		for (int j = 0; j < this->n; j++){
			if (this->board[i][j] != '.')
				continue;
			this->board[i][j] = this->my;
			this->score += this->value[i][j];
			nextv = this->MinValue(number + 1, depth + 1);
			if (nextv > v || (nextv == v && nowType == 'R')){
				v = nextv;
				nowType = 'S';
				nowX = i;
				nowY = j;
			}
			bool s[4];
			if (this->CheckRaid(i, j, s, this->my)){
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->my;
						this->score += 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
				nextv = this->MinValue(number + 1, depth + 1);
				if (nextv > v){
					v = nextv;
					nowType = 'R';
					nowX = i;
					nowY = j;
				}
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->op;
						this->score -= 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
			}
			this->board[i][j] = '.';
			this->score -= this->value[i][j];
		}
	}
	if (depth == 1){
		this->ansX = nowX;
		this->ansY = nowY;
		this->type = nowType;
	}
	return v;
}
int Game::MinValue(int number, int depth){
	if (number == this->n * this->n || depth == this->depth + 1)
		return this->score;
	int v = INT_MAX;
	char nowType;
	int nextv;
	for (int i = 0; i < this->n; i++){
		for (int j = 0; j < this->n; j++){
			if (this->board[i][j] != '.')
				continue;
			this->board[i][j] = this->op;
			this->score -= this->value[i][j];
			nextv = this->MaxValue(number + 1, depth + 1);
			if (nextv < v || (nextv == v && nowType == 'R')){
				v = nextv;
				nowType = 'S';
			}
			bool s[4];
			if (this->CheckRaid(i, j, s, this->op)){
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->op;
						this->score -= 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
				nextv = this->MaxValue(number + 1, depth + 1);
				if (nextv < v){
					v = nextv;
					nowType = 'R';
				}
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->my;
						this->score += 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
			}
			this->board[i][j] = '.';
			this->score += this->value[i][j];
		}
	}
	return v;
}
int Game::MaxValueAlphaBeta(int number, int depth, int alpha, int beta){
	if (number == this->n * this->n || depth == this->depth + 1)
		return this->score;
	int v = INT_MIN;
	char nowType;
	int nowX, nowY, nextv;
	for (int i = 0; i < this->n; i++){
		for (int j = 0; j < this->n; j++){
			if (this->board[i][j] != '.')
				continue;
			this->board[i][j] = this->my;
			this->score += this->value[i][j];
			nextv = this->MinValueAlphaBeta(number + 1, depth + 1, alpha, beta);
			if (nextv > v || (nextv == v && nowType == 'R')){
				v = nextv;
				nowType = 'S';
				nowX = i;
				nowY = j;
			}
			if (v > beta){
				this->board[i][j] = '.';
				this->score -= this->value[i][j];
				return v;
			}
			alpha = max(alpha, v);
			bool s[4];
			if (this->CheckRaid(i, j, s, this->my)){
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->my;
						this->score += 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
				nextv = this->MinValueAlphaBeta(number + 1, depth + 1, alpha, beta);
				if (nextv > v){
					v = nextv;
					nowType = 'R';
					nowX = i;
					nowY = j;
				}
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->op;
						this->score -= 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
			}
			this->board[i][j] = '.';
			this->score -= this->value[i][j];
			if (v > beta)
				return v;
			alpha = max(alpha, v);
		}
	}
	if (depth == 1){
		this->ansX = nowX;
		this->ansY = nowY;
		this->type = nowType;
	}
	return v;
}
int Game::MinValueAlphaBeta(int number, int depth, int alpha, int beta){
	if (number == this->n * this->n || depth == this->depth + 1)
		return this->score;
	int v = INT_MAX;
	char nowType;
	int nextv;
	for (int i = 0; i < this->n; i++){
		for (int j = 0; j < this->n; j++){
			if (this->board[i][j] != '.')
				continue;
			this->board[i][j] = this->op;
			this->score -= this->value[i][j];
			nextv = this->MaxValueAlphaBeta(number + 1, depth + 1, alpha, beta);
			if (nextv < v || (nextv == v && nowType == 'R')){
				v = nextv;
				nowType = 'S';
			}
			if (v < alpha){
				this->board[i][j] = '.';
				this->score += this->value[i][j];
				return v;
			}
			beta = min(beta, v);
			bool s[4];
			if (this->CheckRaid(i, j, s, this->op)){
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->op;
						this->score -= 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
				nextv = this->MaxValueAlphaBeta(number + 1, depth + 1, alpha, beta);
				if (nextv < v){
					v = nextv;
					nowType = 'R';
				}
				for (int k = 0; k < 4; k++){
					if (s[k]){
						this->board[i + this->way[k][0]][j + this->way[k][1]] = this->my;
						this->score += 2 * this->value[i + this->way[k][0]][j + this->way[k][1]];
					}
				}
			}
			this->board[i][j] = '.';
			this->score += this->value[i][j];
			if (v < alpha)
				return v;
			beta = min(beta, v);
		}
	}
	return v;
}

bool Game::CheckRaid(int x, int y, bool* move, char mypiece){
	bool flag1 = false;
	bool flag2 = false;
	for (int i = 0; i < 4; i++){
		move[i] = false;
		int xx = x + this->way[i][0];
		int yy = y + this->way[i][1];
		if (xx < 0 || xx >= this->n || yy < 0 || yy >= this->n || this->board[xx][yy] == '.')
			continue;
		if (this->board[xx][yy] == mypiece){
			flag1 = true;
		}
		else{
			flag2 = true;
			move[i] = true;
		}
	}
	return flag1 && flag2;
}

int main(){
	Game* a = new Game();

	a->Search();
	a->Print();
	return 1;
}