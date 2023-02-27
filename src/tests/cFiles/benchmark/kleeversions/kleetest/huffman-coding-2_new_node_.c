#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	int freq;
	klee_make_symbolic(&freq, sizeof(freq), "df6c5fa731c34c42a3ec359bcb9f2805");
	if ((freq<-1) || (freq>1024)) {
		 return 0;}

	char c;
	klee_make_symbolic(&c, sizeof(c), "78b5569acdc6438c977dc636830b2b08");

	node a;
	klee_make_symbolic(&a, sizeof(a), "52cdd87468324ee388c49f44871cc07b");

	node b;
	klee_make_symbolic(&b, sizeof(b), "564dc1dfa42f4074a99268aeccfa1238");
	return new_node(freq, c, a, b);
}
