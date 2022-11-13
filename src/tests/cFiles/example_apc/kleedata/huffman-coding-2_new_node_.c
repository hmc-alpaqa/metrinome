#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	int freq;
	klee_make_symbolic(&freq, sizeof(freq), "b2136a97811245bcb5c30f98c886be6d");
	if ((freq<-1) || (freq>1024)) {
		 return 0;}

	char c;
	klee_make_symbolic(&c, sizeof(c), "015a33393a8a420e9702f61e526e6740");

	node a;
	klee_make_symbolic(&a, sizeof(a), "dcd203f4e0f04ddf8bfdf505a4298718");

	node b;
	klee_make_symbolic(&b, sizeof(b), "96cc0b1be1204853b6c7566f90f76dee");
	return new_node(freq, c, a, b);
}
