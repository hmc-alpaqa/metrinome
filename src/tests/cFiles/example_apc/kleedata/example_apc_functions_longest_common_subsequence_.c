#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "16ac2cb7ecba48b59250fbc1f97da617");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "4670c4c0adea43e7b88ce4d88b64c165");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "b21ad9a2696d4889ad03b1847d4af721");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "baae1073391c4e18ae282c938e69d54a");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_subsequence(a, b, a_len, b_len);
}
