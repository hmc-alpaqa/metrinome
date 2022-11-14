#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/abc-problem.c>
#define SIZE 10
int main() {

	char **b;
	klee_make_symbolic(&b, sizeof(b), "fc3d943f57fe4a9e8b7987b7f257bd7b");

	char *word;
	klee_make_symbolic(&word, sizeof(word), "f5c16b9c8fc04b1a8b36957918a136fb");
	return can_make_words(b, word);
}
