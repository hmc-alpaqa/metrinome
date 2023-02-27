#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/reverse-words-in-a-string.c>
#define SIZE 10
int main() {

	char *s;
	klee_make_symbolic(&s, sizeof(s), "88ec6cde14894948a1fd199ee923227b");

	int n;
	klee_make_symbolic(&n, sizeof(n), "ef816b88549448ff8e1a9b8f0ace38c3");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	rev_print(s, n);
	return 0;
}
