#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	int a;
	klee_make_symbolic(&a, sizeof(a), "df3a6982f56048e0aeae437ac5374dc7");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	int b;
	klee_make_symbolic(&b, sizeof(b), "b79506068c9944448e8d744aa098ac5d");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return gcd(a, b);
}
