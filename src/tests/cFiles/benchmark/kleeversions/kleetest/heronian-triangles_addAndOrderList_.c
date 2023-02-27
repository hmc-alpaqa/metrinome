#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	list *a;
	klee_make_symbolic(&a, sizeof(a), "e1454af354794131a14184fa95360fe8");

	triangle t;
	klee_make_symbolic(&t, sizeof(t), "d66305c0658544339548bdbd11c2d866");
	addAndOrderList(a, t);
	return 0;
}
