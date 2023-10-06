#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "47c5ec9d0d9648548ca380af1d98454b");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int show;
	klee_make_symbolic(&show, sizeof(show), "36bfc56e4c774c23b8ede7ccbc6f637e");
	if ((show<-1) || (show>1024)) {
		 return 0;}
	return gen_n(n, show);
}
