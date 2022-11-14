#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/quickselect-algorithm.c>
#define SIZE 10
int main() {

	int *v;
	klee_make_symbolic(&v, sizeof(v), "1d2fe2a3260047bdb559b4edc4cea451");

	int len;
	klee_make_symbolic(&len, sizeof(len), "273c9876a22249728882e360bc0fc35b");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "34acf618278644d2890aaec85a5bd4ed");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return qselect(v, len, k);
}
