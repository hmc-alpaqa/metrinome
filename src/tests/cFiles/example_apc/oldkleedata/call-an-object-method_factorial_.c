#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/call-an-object-method.c>
#define SIZE 10
int main() {

	int num;
	klee_make_symbolic(&num, sizeof(num), "24e2c68edc4d4ebda0d41219a925f7d2");
	if ((num<-1) || (num>1024)) {
		 return 0;}
	return factorial(num);
}
