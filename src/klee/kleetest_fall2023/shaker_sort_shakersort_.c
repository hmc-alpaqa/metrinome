#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/shaker_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "2221ae76981b4336ae24fd0a9cd3f397");

	int n;
	klee_make_symbolic(&n, sizeof(n), "682d2f0afd344f5ebecb512cb66288ce");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	shakersort(a, n);
	return 0;
}
