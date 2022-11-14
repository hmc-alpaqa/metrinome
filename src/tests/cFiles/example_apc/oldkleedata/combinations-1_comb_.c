#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/combinations-1.c>
#define SIZE 10
int main() {

	int pool;
	klee_make_symbolic(&pool, sizeof(pool), "03f5c612eac64e43b311ea20d8f43953");
	if ((pool<-1) || (pool>1024)) {
		 return 0;}

	int need;
	klee_make_symbolic(&need, sizeof(need), "1a3c2b4bb16843dca9f0247dc786bbc5");
	if ((need<-1) || (need>1024)) {
		 return 0;}

	marker chosen;
	klee_make_symbolic(&chosen, sizeof(chosen), "c9057d71e1d84703ad4e8097189b998e");

	int at;
	klee_make_symbolic(&at, sizeof(at), "6e7fbed864f24d578aa7b304cd7f5da4");
	if ((at<-1) || (at>1024)) {
		 return 0;}
	comb(pool, need, chosen, at);
	return 0;
}
