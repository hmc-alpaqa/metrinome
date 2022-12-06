#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "4dbfa26755c54cfbad29653bd069882d");
	clean(list);
	return 0;
}
