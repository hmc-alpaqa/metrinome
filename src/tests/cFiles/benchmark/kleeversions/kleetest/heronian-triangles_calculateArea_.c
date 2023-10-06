#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	triangle *t;
	klee_make_symbolic(&t, sizeof(t), "e39f0062bbb54533b2e00361858cf4e1");
	calculateArea(t);
	return 0;
}
