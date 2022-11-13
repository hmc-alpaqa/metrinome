#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/chinese-remainder-theorem.c>
#define SIZE 10
int main() {

	int a;
	klee_make_symbolic(&a, sizeof(a), "44dc53767b084ab98b00e86f3086a488");
	if ((a<-1) || (a>1024)) {
		 return 0;}

	int b;
	klee_make_symbolic(&b, sizeof(b), "d979d20789f24a6fa05ae3699212342b");
	if ((b<-1) || (b>1024)) {
		 return 0;}
	return mul_inv(a, b);
}
