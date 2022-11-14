#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	unsigned int n;
	klee_make_symbolic(&n, sizeof(n), "f4f1ed032af4485b87b7768c2c47b423");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return sum_square_digits(n);
}
