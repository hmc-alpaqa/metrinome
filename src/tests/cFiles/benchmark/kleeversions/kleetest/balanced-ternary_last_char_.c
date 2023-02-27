#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	char *ptr;
	klee_make_symbolic(&ptr, sizeof(ptr), "f4994867d4df4be39920b6b4472d78ec");
	return last_char(ptr);
}
