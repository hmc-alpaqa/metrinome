#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "0bd37cd475844fbbb5b59df894089d97");

	int root;
	klee_make_symbolic(&root, sizeof(root), "cbf04d135d0642a7b44b72d5b119261e");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "1da57c779b8d433688882fc730d6f3c5");
	return newtons_method_iter(number, root, guess);
}
