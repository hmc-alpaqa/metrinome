#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "7c262874170243ddb1b0a0a3db1b76bb");

	int root;
	klee_make_symbolic(&root, sizeof(root), "80025599892a4b23b5299f3980868939");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "78492ea2bc994f8e85b29c0ab87464e6");
	return newtons_method_rec(number, root, guess);
}
