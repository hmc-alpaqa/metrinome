#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/merge_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "49339dbfdff544bca503f6e26e6472df");

	int n;
	klee_make_symbolic(&n, sizeof(n), "cca35f6e7ca14b8480aa666ed36374fc");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int l;
	klee_make_symbolic(&l, sizeof(l), "f5ee739dfec043dda4ee42a13ac44373");
	if ((l<-1) || (l>1024)) {
		 return 0;}

	int r;
	klee_make_symbolic(&r, sizeof(r), "11119af5c68248c89bd42f3a87be5492");
	if ((r<-1) || (r>1024)) {
		 return 0;}
	merge_sort(a, n, l, r);
	return 0;
}
