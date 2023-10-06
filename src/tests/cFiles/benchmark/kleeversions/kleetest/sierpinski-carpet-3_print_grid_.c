#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	char **b;
	klee_make_symbolic(&b, sizeof(b), "7818d8a790fd49f0ab91bf41f43b3702");

	int size;
	klee_make_symbolic(&size, sizeof(size), "287de3d826ec4dcdbf10e9c3aef35198");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	print_grid(b, size);
	return 0;
}
