#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	int base;
	klee_make_symbolic(&base, sizeof(base), "2845972bbf41469ba650ac7b7c4ecc94");
	if ((base<-1) || (base>1024)) {
		 return 0;}

	int expo;
	klee_make_symbolic(&expo, sizeof(expo), "ab5805f559be447bac20f14e19714037");
	if ((expo<-1) || (expo>1024)) {
		 return 0;}
	return intpow(base, expo);
}
