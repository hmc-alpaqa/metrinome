#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	triangle *t;
	klee_make_symbolic(&t, sizeof(t), "8475d49d04254fcdad439b6189c395c3");
	calculateArea(t);
	return 0;
}
