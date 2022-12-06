#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "ba6bc423758e4222b03fa1df1cd8e0a5");
	return checkHouses(ha);
}
