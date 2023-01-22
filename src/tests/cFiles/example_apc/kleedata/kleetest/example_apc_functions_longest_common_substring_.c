#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "6bf0f975acb24939964fbd3529891444");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "7e8bacf0fd5740e1b27328acb237cc4d");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "495b2730de6a485d91c03bd3d99e6e3b");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "6dda4850f98e4cc3996c19d1554724b7");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_substring(a, b, a_len, b_len);
}
