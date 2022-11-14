#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	PartialGrid G;
	klee_make_symbolic(&G, sizeof(G), "758f4653bc564464a28f438d0b187dc0");

	int iterations;
	klee_make_symbolic(&iterations, sizeof(iterations), "ec2a0a67eb544716a2cced7313b2b88e");
	if ((iterations<-1) || (iterations>1024)) {
		 return 0;}
	sierpinski(G, iterations);
	return 0;
}
