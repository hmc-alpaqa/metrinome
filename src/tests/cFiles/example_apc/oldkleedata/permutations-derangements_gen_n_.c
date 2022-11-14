#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "94c9f4b7f7bb4e5aabf21295821ebb0a");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int show;
	klee_make_symbolic(&show, sizeof(show), "5383be591a6f42108ee12fffb684d82e");
	if ((show<-1) || (show>1024)) {
		 return 0;}
	return gen_n(n, show);
}
