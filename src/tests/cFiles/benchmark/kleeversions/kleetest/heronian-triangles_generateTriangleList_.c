#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	int maxSide;
	klee_make_symbolic(&maxSide, sizeof(maxSide), "0f2e727601b941edb3f946d44d12b74e");
	if ((maxSide<-1) || (maxSide>1024)) {
		 return 0;}

	int *count;
	klee_make_symbolic(&count, sizeof(count), "d8eb9b54ca754db0a2afc97dede75174");
	return generateTriangleList(maxSide, count);
}
