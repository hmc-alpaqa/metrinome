#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	char *a;
	klee_make_symbolic(&a, sizeof(a), "a614bc3795cb4677b5835bb3bcb90ae6");

	char *b;
	klee_make_symbolic(&b, sizeof(b), "ce69698308f64cf5a7d966b04eb1c461");

	int a_len;
	klee_make_symbolic(&a_len, sizeof(a_len), "748d0867a19f4dfab692963b2c7e0738");
	if ((a_len<-1) || (a_len>1024)) {
		 return 0;}

	int b_len;
	klee_make_symbolic(&b_len, sizeof(b_len), "6f3eebc3d84e45adad5647c79024c887");
	if ((b_len<-1) || (b_len>1024)) {
		 return 0;}
	return longest_common_subsequence(a, b, a_len, b_len);
}
