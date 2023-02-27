#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutation-test-1.c>
#define SIZE 10
int main() {

	int at;
	klee_make_symbolic(&at, sizeof(at), "ff31ad9c0f4a4e7e98973b298a379919");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int remain;
	klee_make_symbolic(&remain, sizeof(remain), "b86fdd4d583944bab0062f44a6152e9a");
	if ((remain<-1) || (remain>1024)) {
		 return 0;}

	int accu;
	klee_make_symbolic(&accu, sizeof(accu), "4c36d33242eb40eba36161261aeb9f8f");
	if ((accu<-1) || (accu>1024)) {
		 return 0;}

	int treat;
	klee_make_symbolic(&treat, sizeof(treat), "d61cd9ca529b4ce0a36bec0ffde0edeb");
	if ((treat<-1) || (treat>1024)) {
		 return 0;}
	return pick(at, remain, accu, treat);
}
