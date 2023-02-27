#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/combinations-1.c>
#define SIZE 10
int main() {

	int pool;
	klee_make_symbolic(&pool, sizeof(pool), "0266d4af24204e82b52e3819af75ee9f");
	if ((pool<-1) || (pool>1024)) {
		 return 0;}

	int need;
	klee_make_symbolic(&need, sizeof(need), "dde5917d42964198828b40472c5c93ec");
	if ((need<-1) || (need>1024)) {
		 return 0;}

	marker chosen;
	klee_make_symbolic(&chosen, sizeof(chosen), "34a702305ca9426faf38efa78cba6b08");

	int at;
	klee_make_symbolic(&at, sizeof(at), "db2dae593d52402a903d8d6cea496b69");
	if ((at<-1) || (at>1024)) {
		 return 0;}
	comb(pool, need, chosen, at);
	return 0;
}
