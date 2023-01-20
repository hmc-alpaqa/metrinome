#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "b93cbd5c54c443f38c67c97b580ed5ee");

	int root;
	klee_make_symbolic(&root, sizeof(root), "c577b9f425d84ebc8d98fad53488ff90");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "5a569c8008aa4924bba82d4e7c4b8778");
	return newtons_method_iter(number, root, guess);
}
