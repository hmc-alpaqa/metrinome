#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "1a532ce410794dc98c98c1528a36d6de");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "7dbd66111786479bb0bcb5e080da3e00");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "b0cbade2bdbd4b4da6aa543dc6fd6fa1");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "252ad7c49dbe4164b890f85a6df63e28");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_subsequence(a, b, a_len, b_len);
}
