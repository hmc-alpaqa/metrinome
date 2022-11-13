#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/stern-brocot-sequence-1.c>
#define SIZE 10
int main() {

	uint a;
	klee_make_symbolic(&a, sizeof(a), "ca7778aba3944391a1afb72dea4fafbe");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	uint b;
	klee_make_symbolic(&b, sizeof(b), "1426fc521441438490a0397b729647c7");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return gcd(a, b);
}
