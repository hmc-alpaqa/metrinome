#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/bogo_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "1a39a282dd324e9d902710987e979341");

	int n;
	klee_make_symbolic(&n, sizeof(n), "21840d76cea149b3b15cd15d340e63cf");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	sort(a, n);
	return 0;
}
