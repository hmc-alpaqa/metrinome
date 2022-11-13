#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int person;
	klee_make_symbolic(&person, sizeof(person), "e4f57928454247fb9c3dd124edac907b");
	if ((person<-1) || (person>1024)) {
		 return 0;}
	return solve(person);
}
