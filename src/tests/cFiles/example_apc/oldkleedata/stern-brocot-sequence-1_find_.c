#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/stern-brocot-sequence-1.c>
#define SIZE 10
int main() {

	uint from;
	klee_make_symbolic(&from, sizeof(from), "90d4a1f6b8a84dc1a026f87e8f351efa");
	if ((from<-1) || (from>1024)) {
		 return 0;}

	uint to;
	klee_make_symbolic(&to, sizeof(to), "034c01aac44a476f834de68473b22237");
	if ((to<-1) || (to>1024)) {
		 return 0;}
	find(from, to);
	return 0;
}
