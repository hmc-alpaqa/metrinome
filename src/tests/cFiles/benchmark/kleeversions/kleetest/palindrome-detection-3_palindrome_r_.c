#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/palindrome-detection-3.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "1a8a6d2587eb4c48b7078cdc9dd5fcc3");

	int b;
	klee_make_symbolic(&b, sizeof(b), "d339053692d245148bfba4672394c5d2");
	if ((b<-1) || (b>1024)) {
		 return 0;}

	int e;
	klee_make_symbolic(&e, sizeof(e), "0811f18c0bb4424684ac0e86d15891cb");
	if ((e<-1) || (e>1024)) {
		 return 0;}
	return palindrome_r(s, b, e);
}
