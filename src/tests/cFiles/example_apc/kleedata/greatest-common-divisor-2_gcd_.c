#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/greatest-common-divisor-2.c>
#define SIZE 10
int main() {

	int u;
	klee_make_symbolic(&u, sizeof(u), "c98140313d2b4ee0972b738ccc8aaeea");
	if ((u<-1) || (u>1024)) {
		 return 0;}

	int v;
	klee_make_symbolic(&v, sizeof(v), "b5f5b0afd24a42e6bf88a23fff1d1c6f");
	if ((v<-1) || (v>1024)) {
		 return 0;}
	return gcd(u, v);
}
