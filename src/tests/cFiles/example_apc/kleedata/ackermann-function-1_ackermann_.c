#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ackermann-function-1.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "46a762abd49d41889e64b836e6f10a0b");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "8cedf42e64b041abbf7bf02b52954231");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann(m, n);
}
