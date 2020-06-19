#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/06_palindrome.c>
#define SIZE 100
int main() {

	int num;
	klee_make_symbolic(&num, sizeof(num), "4fd2fffea215406283d9720a206900f6");
	return palindrome(num);
}
