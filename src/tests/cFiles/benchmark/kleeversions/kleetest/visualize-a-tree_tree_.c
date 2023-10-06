#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/visualize-a-tree.c>
#define SIZE 10
int main() {

	int root;
	klee_make_symbolic(&root, sizeof(root), "157cc1bad3594574bb1c69b6154c0ff8");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	stem head;
	klee_make_symbolic(&head, sizeof(head), "ed36d69b40f747c193edeb3e3fa8bd8a");
	tree(root, head);
	return 0;
}
