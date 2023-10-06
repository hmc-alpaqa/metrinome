#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	expr e;
	klee_make_symbolic(&e, sizeof(e), "a45b4ec6ed8e42988400b29dc1430e8e");

	frac res;
	klee_make_symbolic(&res, sizeof(res), "e36d48a0e89848cba23b5fa8017c5349");
	eval_tree(e, res);
	return 0;
}
