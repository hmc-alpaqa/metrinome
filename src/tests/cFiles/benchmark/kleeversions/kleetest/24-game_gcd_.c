#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "09753b0366a445289eeed2294656ec0f");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "0b2373f88be64864917199c9087b64d8");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return gcd(m, n);
}
