#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/reverse-words-in-a-string.c>
#define SIZE 10
int main() {

	char *s;
	klee_make_symbolic(&s, sizeof(s), "aca34243954148389165d6994f5d7067");

	int n;
	klee_make_symbolic(&n, sizeof(n), "f4caaaa048c24fc8b35e9092b9ba202c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	rev_print(s, n);
	return 0;
}
