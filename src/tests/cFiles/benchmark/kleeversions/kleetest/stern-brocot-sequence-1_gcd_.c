#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/stern-brocot-sequence-1.c>
#define SIZE 10
int main() {

	uint a;
	klee_make_symbolic(&a, sizeof(a), "28ad3e7b3f4746ea88d259546f9f7bdd");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	uint b;
	klee_make_symbolic(&b, sizeof(b), "c739fd5fab8b4fb4a51d4682fc193887");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return gcd(a, b);
}
