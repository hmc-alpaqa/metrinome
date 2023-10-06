#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/non-continuous-subsequences-3.c>
#define SIZE 10
int main() {

	sint n;
	klee_make_symbolic(&n, sizeof(n), "d8c237bd2fa14b56aa7a0875f5a87ca7");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	sint step;
	klee_make_symbolic(&step, sizeof(step), "777315befb1043b482dbe70a08cfdec3");
	if ((step<-1) || (step>1024)) {
		 return 0;}

	sint state;
	klee_make_symbolic(&state, sizeof(state), "f6d22e8a7da849bbb2b153be53124890");
	if ((state<-1) || (state>1024)) {
		 return 0;}

	char **v;
	klee_make_symbolic(&v, sizeof(v), "669477f9078e43878dceec2ee54e1b0f");

	unsigned long bits;
	klee_make_symbolic(&bits, sizeof(bits), "735cf939f35a41e58008a26d017ba07a");
	pick(n, step, state, v, bits);
	return 0;
}
