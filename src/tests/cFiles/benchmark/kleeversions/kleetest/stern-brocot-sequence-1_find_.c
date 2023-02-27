#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/stern-brocot-sequence-1.c>
#define SIZE 10
int main() {

	uint from;
	klee_make_symbolic(&from, sizeof(from), "681af882207144b8936bc11538273c84");
	if ((from<-1) || (from>1024)) {
		 return 0;}

	uint to;
	klee_make_symbolic(&to, sizeof(to), "03eae79e3fd04e2596b99bf6c638934c");
	if ((to<-1) || (to>1024)) {
		 return 0;}
	find(from, to);
	return 0;
}
