#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/truncatable-primes-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "258199b3d60a48268b4bb32236b2b5ee");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int tens;
	klee_make_symbolic(&tens, sizeof(tens), "6933c99928af4cdca088d55214db4074");
	if ((tens<-1) || (tens>1024)) {
		 return 0;}
	left(n, tens);
	return 0;
}
