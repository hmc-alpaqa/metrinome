#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "3316f6a8d7a74705864399497e1a8ee6");

	char c;
	klee_make_symbolic(&c, sizeof(c), "13b91821fdae4dd1a9d15a82309fc5cc");
	return addEl(list, c);
}
