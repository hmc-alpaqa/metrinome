#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/n-queens-problem-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "034c4c25e2594c2587f66011084bef56");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int col;
	klee_make_symbolic(&col, sizeof(col), "fa94d5a798764af7bce901d491dd60b2");
	if ((col<-1) || (col>1024)) {
		 return 0;}

	int *hist;
	klee_make_symbolic(&hist, sizeof(hist), "6ac8ed52f33f4123b6be6889fd156097");
	solve(n, col, hist);
	return 0;
}
