#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	int a;
	klee_make_symbolic(&a, sizeof(a), "b7618cfc3bf64adea247a5f98f770468");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	int b;
	klee_make_symbolic(&b, sizeof(b), "f9b7a87d918745439f6ed4071ed084c6");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return gcd(a, b);
}
