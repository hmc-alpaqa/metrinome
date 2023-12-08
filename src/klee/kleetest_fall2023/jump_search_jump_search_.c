#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/jump_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	const int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "9732169966914014aac4072754697d19");

	int x;
	klee_make_symbolic(&x, sizeof(x), "d925ec1cddbe4c5aaf117281efffbd67");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	size_t n;
	klee_make_symbolic(&n, sizeof(n), "203da0ce71a14c0e97f0f319505f74a8");
	if ((n<=0) || (n>1024)) {
		 return 0;}
	return jump_search(arr, x, n);
}
