#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/towers-of-hanoi-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "ba7186deaecf442fa27a1802a7776eab");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int from;
	klee_make_symbolic(&from, sizeof(from), "98ee92d2725541919b55c055545ed8a1");
	if ((from<-1) || (from>1024)) {
		 return 0;}

	int via;
	klee_make_symbolic(&via, sizeof(via), "ef3d8807f29e4ded97d1e0d9b8c38ef1");
	if ((via<-1) || (via>1024)) {
		 return 0;}

	int to;
	klee_make_symbolic(&to, sizeof(to), "bf338caef81c483facc6cfb638f61c75");
	if ((to<-1) || (to>1024)) {
		 return 0;}
	move(n, from, via, to);
	return 0;
}
