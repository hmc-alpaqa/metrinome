#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int person;
	klee_make_symbolic(&person, sizeof(person), "653f2d570a464677b3630c901613fe00");
	if ((person<-1) || (person>1024)) {
		 return 0;}
	return solve(person);
}
