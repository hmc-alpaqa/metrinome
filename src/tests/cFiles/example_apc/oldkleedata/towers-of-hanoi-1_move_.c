#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/towers-of-hanoi-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "3180302a9f704bd394238ae943595982");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int from;
	klee_make_symbolic(&from, sizeof(from), "acadf34475544eb2b4e310eca1776688");
	if ((from<-1) || (from>1024)) {
		 return 0;}

	int via;
	klee_make_symbolic(&via, sizeof(via), "9ac6eadfe851439eac0d375e0cf78fef");
	if ((via<-1) || (via>1024)) {
		 return 0;}

	int to;
	klee_make_symbolic(&to, sizeof(to), "11643ff717494c25930cc53ecf456aba");
	if ((to<-1) || (to>1024)) {
		 return 0;}
	move(n, from, via, to);
	return 0;
}
