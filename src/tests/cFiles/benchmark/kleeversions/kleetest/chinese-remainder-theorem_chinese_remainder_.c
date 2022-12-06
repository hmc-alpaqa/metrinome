#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/chinese-remainder-theorem.c>
#define SIZE 10
int main() {

	int *n;
	klee_make_symbolic(&n, sizeof(n), "23e72574213c491da2406339ad186c9c");

	int *a;
	klee_make_symbolic(&a, sizeof(a), "c7e2bdcbbffb49c08f514f18a2226d3f");

	int len;
	klee_make_symbolic(&len, sizeof(len), "9b09bbf6e1ef40b4b58dcfa4b506828c");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	return chinese_remainder(n, a, len);
}
