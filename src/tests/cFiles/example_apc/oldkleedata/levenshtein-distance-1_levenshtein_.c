#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/levenshtein-distance-1.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "078b74ce7b2e40e6a1df40b80c40e50e");

	int ls;
	klee_make_symbolic(&ls, sizeof(ls), "031349a474114fdd8030be835035fe3e");
	if ((ls<-1) || (ls>1024)) {
		 return 0;}

	const char *t;
	klee_make_symbolic(&t, sizeof(t), "77c7957fa403412f9cb8a3ccf5af180f");

	int lt;
	klee_make_symbolic(&lt, sizeof(lt), "411803c66fed4b39914c97f0f3576240");
	if ((lt<-1) || (lt>1024)) {
		 return 0;}
	return levenshtein(s, ls, t, lt);
}
