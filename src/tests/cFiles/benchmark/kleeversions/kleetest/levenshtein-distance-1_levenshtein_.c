#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/levenshtein-distance-1.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "cd11ab1798454a1d8004d22079f9a831");

	int ls;
	klee_make_symbolic(&ls, sizeof(ls), "b1ae3b772111482e8756d867acacd35f");
	if ((ls<-1) || (ls>1024)) {
		 return 0;}

	const char *t;
	klee_make_symbolic(&t, sizeof(t), "f12ddc0c2e544b45ae08c5913e3659da");

	int lt;
	klee_make_symbolic(&lt, sizeof(lt), "6ecfbe43d08145d3a8bd4a0d7e52c852");
	if ((lt<-1) || (lt>1024)) {
		 return 0;}
	return levenshtein(s, ls, t, lt);
}
