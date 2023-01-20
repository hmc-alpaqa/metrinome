#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "2898a69a3d3741848a769746dcb43915");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "d3e99bf09a35444aadb9b52b420cd790");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "048b137a91304eb297c3b6f145d5523c");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "1056469681034f24a2b56b3c337ce4a1");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_substring(a, b, a_len, b_len);
}
