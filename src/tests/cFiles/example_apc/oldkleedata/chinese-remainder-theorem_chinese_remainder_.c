#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/chinese-remainder-theorem.c>
#define SIZE 10
int main() {

	int *n;
	klee_make_symbolic(&n, sizeof(n), "469365a4014d45f3916f687460e24239");

	int *a;
	klee_make_symbolic(&a, sizeof(a), "f9b9e57639f849d08f97a0a3d63d446d");

	int len;
	klee_make_symbolic(&len, sizeof(len), "94f8acda4d90463890170cd35bb85229");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	return chinese_remainder(n, a, len);
}
