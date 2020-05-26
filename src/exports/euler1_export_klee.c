#include <klee/klee.h>
#include </app/code/tests/cFiles/problem1.c>
#define SIZE 10
int main() {

	int s3;
	klee_make_symbolic(&s3, sizeof(s3), "d88a07994e9143c0b309818268752488");

	int s5;
	klee_make_symbolic(&s5, sizeof(s5), "ac79ec6f7b7148878395141c1de54a5a");

	int s15;
	klee_make_symbolic(&s15, sizeof(s15), "0a6118580e114c9d92913afbe6d8ce8a");
	return euler1(s3, s5, s15);
}
