#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/n-queens-problem-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "7fb57cf022a44abab97244ad3a284711");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int col;
	klee_make_symbolic(&col, sizeof(col), "0b3bca84e47b4b06bc6270d9a3d8423a");
	if ((col<-1) || (col>1024)) {
		 return 0;}

	int *hist;
	klee_make_symbolic(&hist, sizeof(hist), "09ae270d11c44cfab16eabacea7d7f95");
	solve(n, col, hist);
	return 0;
}
