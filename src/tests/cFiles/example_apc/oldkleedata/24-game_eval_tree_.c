#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	expr e;
	klee_make_symbolic(&e, sizeof(e), "1a39943db2474586ba2f4d85efdd982c");

	frac res;
	klee_make_symbolic(&res, sizeof(res), "d7c769c10b0a444e9f93669b759e3f6c");
	eval_tree(e, res);
	return 0;
}
