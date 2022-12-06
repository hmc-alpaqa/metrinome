#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/topswops-1.c>
#define SIZE 10
int main() {

	deck *a;
	klee_make_symbolic(&a, sizeof(a), "7c789de88e9447eeb17ff4779a9b48b5");

	uint f;
	klee_make_symbolic(&f, sizeof(f), "f7eed4a5cbc24eb8866eef8616aff0c4");
	if ((f<-1) || (f>1024)) {
		 return 0;}

	uint s;
	klee_make_symbolic(&s, sizeof(s), "9f314807053b4c5899a8e7675922397c");
	if ((s<-1) || (s>1024)) {
		 return 0;}
	tryswaps(a, f, s);
	return 0;
}
