#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	char ***g;
	klee_make_symbolic(&g, sizeof(g), "791b870813384e9a83239fb9a49da44d");

	int n;
	klee_make_symbolic(&n, sizeof(n), "bd9f0c8c42fd4ba7aa84da50fa8f9d32");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	const char sep;
	klee_make_symbolic(&sep, sizeof(sep), "0c38a98873e24e69a6f5eabc64b9f1d1");
	return allocate_grid(g, n, sep);
}
