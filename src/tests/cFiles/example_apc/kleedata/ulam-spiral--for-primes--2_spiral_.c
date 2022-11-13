#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ulam-spiral--for-primes--2.c>
#define SIZE 10
int main() {

	int w;
	klee_make_symbolic(&w, sizeof(w), "10e78204efaf4b918be72dac61d5b3ae");
	if ((w<-1) || (w>1024)) {
		 return 0;}

	int h;
	klee_make_symbolic(&h, sizeof(h), "b786b2c7b01e4a7aa5fa48982edddbc9");
	if ((h<-1) || (h>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "2bd0156aa08d4d3ca5118d39a3263883");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int y;
	klee_make_symbolic(&y, sizeof(y), "fc45b0aa954841dda32c0fa580be21e2");
	if ((y<-1) || (y>1024)) {
		 return 0;}
	return spiral(w, h, x, y);
}
