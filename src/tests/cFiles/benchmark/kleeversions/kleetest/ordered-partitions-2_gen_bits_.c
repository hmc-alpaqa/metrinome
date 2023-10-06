#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ordered-partitions-2.c>
#define SIZE 10
int main() {

	uint mask;
	klee_make_symbolic(&mask, sizeof(mask), "591ac45a03d84ac68b0e93ba10491066");
	if ((mask<-1) || (mask>1024)) {
		 return 0;}

	uint all;
	klee_make_symbolic(&all, sizeof(all), "9c1471321d1a4a048491e13e0772967d");
	if ((all<-1) || (all>1024)) {
		 return 0;}

	uint res;
	klee_make_symbolic(&res, sizeof(res), "6cdfa6694c5b447984655c056a29f59c");
	if ((res<-1) || (res>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "faa19176903d49a98490807c6ff28ca6");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int pid;
	klee_make_symbolic(&pid, sizeof(pid), "ccf3ea14d3454710845cc09fbdedc509");
	if ((pid<-1) || (pid>1024)) {
		 return 0;}
	gen_bits(mask, all, res, n, pid);
	return 0;
}
