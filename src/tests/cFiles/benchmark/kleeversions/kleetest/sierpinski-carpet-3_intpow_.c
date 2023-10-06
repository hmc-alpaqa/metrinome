#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	int base;
	klee_make_symbolic(&base, sizeof(base), "501b05bced4f4df4a6f96ffb10b8fcc7");
	if ((base<-1) || (base>1024)) {
		 return 0;}

	int expo;
	klee_make_symbolic(&expo, sizeof(expo), "81732bff69c847f3a0a647d51c73e2b6");
	if ((expo<-1) || (expo>1024)) {
		 return 0;}
	return intpow(base, expo);
}
