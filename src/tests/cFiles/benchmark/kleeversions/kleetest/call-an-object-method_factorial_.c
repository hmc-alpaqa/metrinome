#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/call-an-object-method.c>
#define SIZE 10
int main() {

	int num;
	klee_make_symbolic(&num, sizeof(num), "fc84af59146c4fee9d64905a82fc6d29");
	if ((num<-1) || (num>1024)) {
		 return 0;}
	return factorial(num);
}
