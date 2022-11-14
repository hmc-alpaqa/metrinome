#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *a;
	klee_make_symbolic(&a, sizeof(a), "6fab05a4452b4488a0cd255f3efb0e94");
	return from_bt(a);
}
