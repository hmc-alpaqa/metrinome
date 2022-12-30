#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	double number;
	klee_make_symbolic(&number, sizeof(number), "60b4e1ffc6e74244858266cfdf21531d");

	int root;
	klee_make_symbolic(&root, sizeof(root), "25ba3c18dfe940ffa2caa47480a3a66e");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	double guess;
	klee_make_symbolic(&guess, sizeof(guess), "095e2762c6524df3b3a57d5add3bcc07");
	return newtons_method_iter(number, root, guess);
}
