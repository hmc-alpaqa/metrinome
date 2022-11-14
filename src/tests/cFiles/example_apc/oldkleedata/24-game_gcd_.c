#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "af770c9de73e4239b7f4142fbeeb6e4f");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "b64d9be94f334d0fad399bbdc210079f");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return gcd(m, n);
}
