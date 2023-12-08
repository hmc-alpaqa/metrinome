#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/random_quick_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "a6716b080a4547009c4f0c6f6afad055");

	int left;
	klee_make_symbolic(&left, sizeof(left), "64eaf76ce0be486a92be9eaca7b79c7b");
	if ((left<-1) || (left>1024)) {
		 return 0;}

	int right;
	klee_make_symbolic(&right, sizeof(right), "4df137afb79141d09831760153c2439e");
	if ((right<-1) || (right>1024)) {
		 return 0;}
	random_quick(a, left, right);
	return 0;
}
