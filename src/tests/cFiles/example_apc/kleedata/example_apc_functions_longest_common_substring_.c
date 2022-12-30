#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "2d0ceb74a4a04d5da0eb1329d22cf040");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "05345911e80c40c5b55d07648018a35d");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "7364e593525c453da6f132320fc30276");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "f4211fb3210649fa95cdb76af572d21b");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_substring(a, b, a_len, b_len);
}
