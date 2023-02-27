#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f5e4a210988d47ee9c8d2876977bec01");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	char *b;
	klee_make_symbolic(&b, sizeof(b), "ca2559474f5743a4a77730089cae0f7a");
	to_bt(n, b);
	return 0;
}
