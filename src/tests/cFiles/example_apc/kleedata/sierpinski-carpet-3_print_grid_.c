#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	char **b;
	klee_make_symbolic(&b, sizeof(b), "a38fa47ddf444c6eb4fbde8d265313af");

	int size;
	klee_make_symbolic(&size, sizeof(size), "2bc907e65a2e447b996238dcdf6932f4");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	print_grid(b, size);
	return 0;
}
