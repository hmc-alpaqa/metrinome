#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "47eaa2faa1874393b2334cc0ed14e76e");

	char c;
	klee_make_symbolic(&c, sizeof(c), "4d5d6f0215f54ac09f4082d5a1d11a5d");
	return addEl(list, c);
}
