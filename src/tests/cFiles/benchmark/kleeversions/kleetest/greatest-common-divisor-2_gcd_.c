#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/greatest-common-divisor-2.c>
#define SIZE 10
int main() {

	int u;
	klee_make_symbolic(&u, sizeof(u), "14ba1f03f2d94fbd9244d9fd5369768d");
	if ((u<-1) || (u>1024)) {
		 return 0;}

	int v;
	klee_make_symbolic(&v, sizeof(v), "b58d931df8c7445a898cc69410fc8a33");
	if ((v<-1) || (v>1024)) {
		 return 0;}
	return gcd(u, v);
}
