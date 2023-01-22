#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "437640240953424f98a237dadec9b292");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return polypath_rec(n);
}
