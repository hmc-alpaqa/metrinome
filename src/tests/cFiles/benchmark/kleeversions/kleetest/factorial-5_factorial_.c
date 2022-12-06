#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "3bc1b056b70a4548a8a2417e0a5e1648");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
