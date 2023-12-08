#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/binary_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	const int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "b65c59f7a7644db2902672bda32bf1c7");

	int l;
	klee_make_symbolic(&l, sizeof(l), "4817480b94324987b061e92d7822e444");
	if ((l<-1) || (l>1024)) {
		 return 0;}

	int r;
	klee_make_symbolic(&r, sizeof(r), "3cd5d6c37fc045fe9d830b1be478fd07");
	if ((r<-1) || (r>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "cdde104f81df46cbbd535deb6a800a0c");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binarysearch1(arr, l, r, x);
}
