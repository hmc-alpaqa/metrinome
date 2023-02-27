#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	node n;
	klee_make_symbolic(&n, sizeof(n), "cf4ebe6845c6495f9f414d2869ceb7b4");

	char *s;
	klee_make_symbolic(&s, sizeof(s), "26d5e136d41a44b5ab31d32b44c3cf6b");

	int len;
	klee_make_symbolic(&len, sizeof(len), "662f8ed99fb14ac4919b11d9ac1804f8");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	build_code(n, s, len);
	return 0;
}
