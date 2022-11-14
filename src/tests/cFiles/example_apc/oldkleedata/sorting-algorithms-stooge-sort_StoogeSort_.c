#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-stooge-sort.c>
#define SIZE 10
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "973f28ddf03343998f34469dfacf73e6");

	int i;
	klee_make_symbolic(&i, sizeof(i), "1ff3bd9a02f04a7f9ea9936889b80022");
	if ((i<-1) || (i>1024)) {
		 return 0;}

	int j;
	klee_make_symbolic(&j, sizeof(j), "1fdd02c7324e46a78e1bf9f2842be0e9");
	if ((j<-1) || (j>1024)) {
		 return 0;}
	StoogeSort(a, i, j);
	return 0;
}
