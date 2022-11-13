#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/topswops-1.c>
#define SIZE 10
int main() {

	deck *a;
	klee_make_symbolic(&a, sizeof(a), "a5952d019ad445919e4b57fcd30032d1");

	uint f;
	klee_make_symbolic(&f, sizeof(f), "1bb47a28bf2f4da790d02363b8a09e45");
	if ((f<-1) || (f>1024)) {
		 return 0;}

	uint s;
	klee_make_symbolic(&s, sizeof(s), "922e90e735604fa48ee81d3547ece646");
	if ((s<-1) || (s>1024)) {
		 return 0;}
	tryswaps(a, f, s);
	return 0;
}
