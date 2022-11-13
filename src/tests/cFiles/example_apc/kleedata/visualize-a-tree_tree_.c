#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/visualize-a-tree.c>
#define SIZE 10
int main() {

	int root;
	klee_make_symbolic(&root, sizeof(root), "fccbac631fc546ba8e8114ad74ec435b");
	if ((root<-1) || (root>1024)) {
		 return 0;}

	stem head;
	klee_make_symbolic(&head, sizeof(head), "04ecbc83f5904a4780f1af117d5631b0");
	tree(root, head);
	return 0;
}
