#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "dd98c81d4a2c41dca601df65bb8f4428");
	printHouses(ha);
	return 0;
}
