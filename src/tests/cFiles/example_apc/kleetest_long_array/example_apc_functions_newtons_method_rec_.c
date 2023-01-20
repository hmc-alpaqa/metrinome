#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "36688317ff5146e886d4e1108bed403a");

	int root;
	klee_make_symbolic(&root, sizeof(root), "70792b4824844418a7ba99061b8bfa94");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "ccfa49bda0fc48f998ad5e85e02c1e92");
	return newtons_method_rec(number, root, guess);
}
