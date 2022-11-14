#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "ffe29560f5144524987ec943842f1854");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	char *b;
	klee_make_symbolic(&b, sizeof(b), "709ae23208e84e38a08f841b1c958493");
	to_bt(n, b);
	return 0;
}
