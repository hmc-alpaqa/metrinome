#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/happy-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "6368e591688a4f2c86ea27c57a1fe962");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return happy(n);
}
