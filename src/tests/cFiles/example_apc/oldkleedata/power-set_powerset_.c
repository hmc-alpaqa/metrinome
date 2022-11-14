#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/power-set.c>
#define SIZE 10
int main() {

	char **v;
	klee_make_symbolic(&v, sizeof(v), "f978ac43a3bc40b4ac0a802c0dded164");

	int n;
	klee_make_symbolic(&n, sizeof(n), "9f41895618444be2af2a12bc5a64766a");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	struct node *up;
	klee_make_symbolic(&up, sizeof(up), "90daf9509adc445d86dabd3cde07cdad");
	powerset(v, n, up);
	return 0;
}
