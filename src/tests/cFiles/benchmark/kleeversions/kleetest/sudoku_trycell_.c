#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sudoku.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "df46ca4e2954437b9ec6907d7dec18ac");

	int pos;
	klee_make_symbolic(&pos, sizeof(pos), "76fe8e0c53244869aa037b24551153f6");
	if ((pos<-1) || (pos>1024)) {
		 return 0;}
	return trycell(x, pos);
}
