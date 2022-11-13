#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "acaed549e3634494ad98213e3ad557a7");
	printHouses(ha);
	return 0;
}
