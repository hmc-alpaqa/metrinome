#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "8952644053b34a569d5079994a481423");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "7b1e5459024a454b9e064668e4803851");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann_rec(m, n);
}
