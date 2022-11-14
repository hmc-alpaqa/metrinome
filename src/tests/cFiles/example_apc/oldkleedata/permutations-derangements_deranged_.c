#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int depth;
	klee_make_symbolic(&depth, sizeof(depth), "c0d5a9a3d14043a09214614abacd9f74");
	if ((depth<-1) || (depth>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "6ebdbeea62fb4ed681fb52989c9d661b");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int *d;
	klee_make_symbolic(&d, sizeof(d), "bbafbd07fbde452c80d6411de51eb4ff");

	int show;
	klee_make_symbolic(&show, sizeof(show), "fee33736768e477da392612514158e02");
	if ((show<-1) || (show>1024)) {
		 return 0;}
	return deranged(depth, len, d, show);
}
