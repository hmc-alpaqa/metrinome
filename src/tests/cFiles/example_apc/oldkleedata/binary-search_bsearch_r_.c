#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/binary-search.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "f670fc675f81400abea53057969e7ce8");

	int x;
	klee_make_symbolic(&x, sizeof(x), "079e22ecdd944ae38ea9e6cc1dfb9dc6");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int i;
	klee_make_symbolic(&i, sizeof(i), "4794c251f89e411d851f533ca301086e");
	if ((i<-1) || (i>1024)) {
		 return 0;}

	int j;
	klee_make_symbolic(&j, sizeof(j), "b9bed6be3aae4356b3d976a47188a0e9");
	if ((j<-1) || (j>1024)) {
		 return 0;}
	return bsearch_r(a, x, i, j);
}
