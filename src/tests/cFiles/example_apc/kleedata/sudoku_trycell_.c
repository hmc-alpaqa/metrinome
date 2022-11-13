#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sudoku.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "30e50ae9cfd54277b471880e9862b5f4");

	int pos;
	klee_make_symbolic(&pos, sizeof(pos), "c5c861065787411c8e2e9eb810ef76da");
	if ((pos<-1) || (pos>1024)) {
		 return 0;}
	return trycell(x, pos);
}
