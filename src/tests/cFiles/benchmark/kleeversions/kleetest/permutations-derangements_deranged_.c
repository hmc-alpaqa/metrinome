#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int depth;
	klee_make_symbolic(&depth, sizeof(depth), "2a11fb6c1c69440b926d059122e77752");
	if ((depth<-1) || (depth>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "c7263aafe4c14c098e885219310e50e6");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int *d;
	klee_make_symbolic(&d, sizeof(d), "c9c7ff341aa542e49a82b2d4c71f78f2");

	int show;
	klee_make_symbolic(&show, sizeof(show), "ee4c638c84c844198a4eaf7b2eea0a0a");
	if ((show<-1) || (show>1024)) {
		 return 0;}
	return deranged(depth, len, d, show);
}
