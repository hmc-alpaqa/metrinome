#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/heap_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "06fa832cf5154359bd8893cf698ca7af");

	int n;
	klee_make_symbolic(&n, sizeof(n), "6cbc379e528f4b5eb6f5ced991a07151");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	heapsort(a, n);
	return 0;
}
