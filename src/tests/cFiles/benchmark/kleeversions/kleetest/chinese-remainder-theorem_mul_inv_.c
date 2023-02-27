#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/chinese-remainder-theorem.c>
#define SIZE 10
int main() {

	int a;
	klee_make_symbolic(&a, sizeof(a), "1a79cd31484a4fc3827ce710fd285642");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	int b;
	klee_make_symbolic(&b, sizeof(b), "0403d19c12c04aea80249bbe9068c94f");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return mul_inv(a, b);
}
