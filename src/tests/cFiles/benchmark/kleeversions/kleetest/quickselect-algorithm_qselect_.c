#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/quickselect-algorithm.c>
#define SIZE 10
int main() {

	int *v;
	klee_make_symbolic(&v, sizeof(v), "34779536bcbf436ab9bb5e06d2f79f80");

	int len;
	klee_make_symbolic(&len, sizeof(len), "9b129718bc04451f834b433ec5d469bd");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "5158e6c68320401e98ba6c8c00e2f366");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return qselect(v, len, k);
}
