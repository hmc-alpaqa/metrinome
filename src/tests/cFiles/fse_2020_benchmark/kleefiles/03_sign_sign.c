#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/03_sign.c>
#define SIZE 100
int main() {

	int num;
	klee_make_symbolic(&num, sizeof(num), "b93f70ddeb8d459cb4358cb177240837");
	return sign(num);
}
