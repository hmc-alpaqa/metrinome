#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-by-swapping.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "b22847ad766f45139a40c12d6a3d0b37");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "f6e3a93fe950488f93d86a0ff615bad2");

	int arrLen;
	klee_make_symbolic(&arrLen, sizeof(arrLen), "1bd954b120ed4b2c938c16cd320d2865");
	if ((arrLen<-1) || (arrLen>1024)) {
		 return 0;}
	heapPermute(n, arr, arrLen);
	return 0;
}
