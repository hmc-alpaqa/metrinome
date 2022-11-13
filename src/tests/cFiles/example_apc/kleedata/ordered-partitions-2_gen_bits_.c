#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ordered-partitions-2.c>
#define SIZE 10
int main() {

	uint mask;
	klee_make_symbolic(&mask, sizeof(mask), "d7e216302faa4ec7931a4bbb566864ca");
	if ((mask<-1) || (mask>1024)) {
		 return 0;}

	uint all;
	klee_make_symbolic(&all, sizeof(all), "8b22fbc3d4bd4230b8fc0807eb8a8fa1");
	if ((all<-1) || (all>1024)) {
		 return 0;}

	uint res;
	klee_make_symbolic(&res, sizeof(res), "b53cefa76177471988221123b0f368ca");
	if ((res<-1) || (res>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "4ab608c60b9b49298881a4678a325b07");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int pid;
	klee_make_symbolic(&pid, sizeof(pid), "dda682aee1bf431cb9324fb7c4fed9ab");
	if ((pid<-1) || (pid>1024)) {
		 return 0;}
	gen_bits(mask, all, res, n, pid);
	return 0;
}
