#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	int maxSide;
	klee_make_symbolic(&maxSide, sizeof(maxSide), "9dbdff425fe94f59ac45329ff7c1ede7");
	if ((maxSide<-1) || (maxSide>1024)) {
		 return 0;}

	int *count;
	klee_make_symbolic(&count, sizeof(count), "2fe73a4a46e843d99282124ebd6b11b2");
	return generateTriangleList(maxSide, count);
}
