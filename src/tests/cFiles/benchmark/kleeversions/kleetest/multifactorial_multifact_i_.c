#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/multifactorial.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c05cbecdeb114653b3181211026bbe8e");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int deg;
	klee_make_symbolic(&deg, sizeof(deg), "233c3b546739460e82432a8dd7e7201d");
	if ((deg<-1) || (deg>1024)) {
		 return 0;}
	return multifact_i(n, deg);
}
