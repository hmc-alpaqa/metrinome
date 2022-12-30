#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "3e1c763be44c4db4b0eb1e7903fe4938");

	int root;
	klee_make_symbolic(&root, sizeof(root), "c63b0d2ae0c243c4b882f2227b6a2780");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "69a9f0da47d641b39200fa38d6302330");
	return newtons_method_iter(number, root, guess);
}
