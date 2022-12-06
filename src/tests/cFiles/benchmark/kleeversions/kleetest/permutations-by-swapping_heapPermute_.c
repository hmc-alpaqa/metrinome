#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-by-swapping.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "959bbe8699b04e029eebee26a589b907");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "6f6eeec2b35d4ab9b962a5272c4ce234");

	int arrLen;
	klee_make_symbolic(&arrLen, sizeof(arrLen), "05b4afa374474ffc85ec0992d53fe3d8");
	if ((arrLen<-1) || (arrLen>1024)) {
		 return 0;}
	heapPermute(n, arr, arrLen);
	return 0;
}
