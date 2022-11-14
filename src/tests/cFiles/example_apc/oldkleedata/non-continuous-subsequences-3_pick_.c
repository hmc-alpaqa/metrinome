#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/non-continuous-subsequences-3.c>
#define SIZE 10
int main() {

	sint n;
	klee_make_symbolic(&n, sizeof(n), "172bb68028b946c997601b16116d19e9");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	sint step;
	klee_make_symbolic(&step, sizeof(step), "f97acd631d6440199faabc649f9a9307");
	if ((step<-1) || (step>1024)) {
		 return 0;}

	sint state;
	klee_make_symbolic(&state, sizeof(state), "b811772e5e93445a89a90e859763cd66");
	if ((state<-1) || (state>1024)) {
		 return 0;}

	char **v;
	klee_make_symbolic(&v, sizeof(v), "70a53ec8be2148d88adf41ef711f6aeb");

	unsigned long bits;
	klee_make_symbolic(&bits, sizeof(bits), "d6ab4a32415341338e05062e2df542f7");
	pick(n, step, state, v, bits);
	return 0;
}
