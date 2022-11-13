#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/truncatable-primes-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "0c04ca4419274be68678832b89c450db");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int tens;
	klee_make_symbolic(&tens, sizeof(tens), "a9785afdf4994668b6e733409066c595");
	if ((tens<-1) || (tens>1024)) {
		 return 0;}
	left(n, tens);
	return 0;
}
