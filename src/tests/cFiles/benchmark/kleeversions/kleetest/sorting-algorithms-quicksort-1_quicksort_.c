#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-1.c>
#define SIZE 10
int main() {

	int *A;
	klee_make_symbolic(&A, sizeof(A), "ebdc5657eedf49f3aab7146b8e117e84");

	int len;
	klee_make_symbolic(&len, sizeof(len), "abadf0ff21f442f3943d60d99e9549cb");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	quicksort(A, len);
	return 0;
}
