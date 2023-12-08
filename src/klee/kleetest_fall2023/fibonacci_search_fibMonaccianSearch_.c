#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/fibonacci_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "1b71785a869146fabe237dee2ee52e25");

	int x;
	klee_make_symbolic(&x, sizeof(x), "858654dd7fc549b2b1d9e88f35e40e4b");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "f35d6f6bf0604cd0944c09514f8d1de0");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fibMonaccianSearch(arr, x, n);
}
