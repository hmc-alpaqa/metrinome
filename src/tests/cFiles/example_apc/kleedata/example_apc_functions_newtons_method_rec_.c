#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "ce7d81e388d84a6da44d44f3617fd761");

	int root;
	klee_make_symbolic(&root, sizeof(root), "553696603ad942d4bd94b8c2e6aca0a2");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "2c0b358745744741a54da95a4b994c66");
	return newtons_method_rec(number, root, guess);
}
