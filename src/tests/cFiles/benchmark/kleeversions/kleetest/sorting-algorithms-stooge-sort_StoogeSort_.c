#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-stooge-sort.c>
#define SIZE 10
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "af4363e3c97a429493517331ba2bb269");

	int i;
	klee_make_symbolic(&i, sizeof(i), "a5e23c5f970d41e3a5d83da6b0438391");
	if ((i<-1) || (i>1024)) {
		 return 0;}

	int j;
	klee_make_symbolic(&j, sizeof(j), "6cff54326ac84b1f8ccc5413e0f88dfe");
	if ((j<-1) || (j>1024)) {
		 return 0;}
	StoogeSort(a, i, j);
	return 0;
}
