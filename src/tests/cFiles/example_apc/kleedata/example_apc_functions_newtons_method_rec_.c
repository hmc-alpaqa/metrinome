#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "92bfbc53a3434d0fa4fc47e0cd5ae4c7");

	int root;
	klee_make_symbolic(&root, sizeof(root), "582d74da197c4e66a64af37eb9edd06f");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "5263c6ddf1cd4e51b4f6f99dc8b60166");
	return newtons_method_rec(number, root, guess);
}
