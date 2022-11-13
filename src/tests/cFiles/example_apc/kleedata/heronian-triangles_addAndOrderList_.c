#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	list *a;
	klee_make_symbolic(&a, sizeof(a), "e7cfbd4e226a48a8aedafef4d6865f1e");

	triangle t;
	klee_make_symbolic(&t, sizeof(t), "c3cd01ca369a4cf8890f0b526ebe6d6d");
	addAndOrderList(a, t);
	return 0;
}
