#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/palindrome-detection-3.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "6f015dc0a36e42449b199503f40d85fb");

	int b;
	klee_make_symbolic(&b, sizeof(b), "69fee45a90534cb7bce2a85392bf66ff");
	if ((b<-1) || (b>1024)) {
		 return 0;}

	int e;
	klee_make_symbolic(&e, sizeof(e), "4e902083a1984f20931a811e2c3ef37e");
	if ((e<-1) || (e>1024)) {
		 return 0;}
	return palindrome_r(s, b, e);
}
