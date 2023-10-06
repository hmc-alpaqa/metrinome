#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ackermann-function-1.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "aa1290a83f6d4bd88960723ca11adaf0");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "eb0c27c412ec49b1b834260dfc96075f");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann(m, n);
}
