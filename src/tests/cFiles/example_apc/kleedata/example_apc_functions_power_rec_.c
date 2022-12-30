#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "5efe048b7fb74e75b0308480e1157422");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "1f6fe485f5634b2fa04f524825729d23");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_rec(x, n);
}
