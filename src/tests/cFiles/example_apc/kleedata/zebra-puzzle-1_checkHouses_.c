#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "41346fbb045244069604690e51abe0e2");
	return checkHouses(ha);
}
