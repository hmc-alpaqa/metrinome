#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	unsigned int n;
	klee_make_symbolic(&n, sizeof(n), "6dbdcc0480364fce8c271ef6c46c51e5");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return sum_square_digits(n);
}
