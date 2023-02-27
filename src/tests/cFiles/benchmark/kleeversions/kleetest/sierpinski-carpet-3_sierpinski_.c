#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	PartialGrid G;
	klee_make_symbolic(&G, sizeof(G), "89997653f4a4451faf8e7fae978d883e");

	int iterations;
	klee_make_symbolic(&iterations, sizeof(iterations), "9d2a16291c31492db9555b21f429a9cc");
	if ((iterations<-1) || (iterations>1024)) {
		 return 0;}
	sierpinski(G, iterations);
	return 0;
}
