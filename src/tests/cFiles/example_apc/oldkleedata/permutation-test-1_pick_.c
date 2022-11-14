#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutation-test-1.c>
#define SIZE 10
int main() {

	int at;
	klee_make_symbolic(&at, sizeof(at), "582cb8687356446b990a639bcc33f74d");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int remain;
	klee_make_symbolic(&remain, sizeof(remain), "e404f36618424424b9ee4c6e46509b4c");
	if ((remain<-1) || (remain>1024)) {
		 return 0;}

	int accu;
	klee_make_symbolic(&accu, sizeof(accu), "cdc6ab5afd9a4579bc18187a89b29b81");
	if ((accu<-1) || (accu>1024)) {
		 return 0;}

	int treat;
	klee_make_symbolic(&treat, sizeof(treat), "ea9c003ac8b84549b5ff9d614043e7d1");
	if ((treat<-1) || (treat>1024)) {
		 return 0;}
	return pick(at, remain, accu, treat);
}
