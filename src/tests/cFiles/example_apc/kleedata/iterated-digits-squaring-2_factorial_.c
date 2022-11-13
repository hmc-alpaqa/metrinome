#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "854f762e5eec43f3b5a2a8f04b6d9eaf");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
