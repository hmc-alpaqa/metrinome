#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "c0f771892c814a138e29855e9d246b32");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "4deed0ccb545439ea446e392db571c60");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_iter(x, n);
}
