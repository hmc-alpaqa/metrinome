#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/abc-problem.c>
#define SIZE 10
int main() {

	char **b;
	klee_make_symbolic(&b, sizeof(b), "807de10f818b467ea4c2a0b5b73123e7");

	char *word;
	klee_make_symbolic(&word, sizeof(word), "799e1d50c32741a7b150075cf1be9554");
	return can_make_words(b, word);
}
