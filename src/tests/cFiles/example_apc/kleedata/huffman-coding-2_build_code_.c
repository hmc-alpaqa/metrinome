#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	node n;
	klee_make_symbolic(&n, sizeof(n), "b5ffa8030329473e8dd275c9c0b52e1d");

	char *s;
	klee_make_symbolic(&s, sizeof(s), "07168c47e6e0494d97c522bb9329d390");

	int len;
	klee_make_symbolic(&len, sizeof(len), "2dbeb435ddd24d8d81c6b6ff7a60bc50");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	build_code(n, s, len);
	return 0;
}
