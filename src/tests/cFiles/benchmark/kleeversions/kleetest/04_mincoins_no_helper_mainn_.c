#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/04_mincoins_no_helper.c>
#define SIZE 10
int main() {

	int cost;
	klee_make_symbolic(&cost, sizeof(cost), "769920c70f7a46e79780d98d2feeab3a");
	if ((cost<-1) || (cost>1024)) {
		 return 0;}
	return mainn(cost);
}
