#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	char ***g;
	klee_make_symbolic(&g, sizeof(g), "00fa324bc0464c59b9ea47cfbe0e7f28");

	int n;
	klee_make_symbolic(&n, sizeof(n), "8381973cfe304a4c95bcbb3f959881e3");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	const char sep;
	klee_make_symbolic(&sep, sizeof(sep), "1ea7baee0ec34cc3a87af0093155ef4a");
	return allocate_grid(g, n, sep);
}
