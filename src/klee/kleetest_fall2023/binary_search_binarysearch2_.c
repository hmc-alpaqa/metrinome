#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/binary_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	const int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "04b0399d6eb947658dadd62581c1ab3a");

	int l;
	klee_make_symbolic(&l, sizeof(l), "7d89c80aa2284f91a0ffc8a9466f1f6f");
	if ((l<-1) || (l>1024)) {
		 return 0;}

	int r;
	klee_make_symbolic(&r, sizeof(r), "68590157ad7545a8a7cef26f51f1ec94");
	if ((r<-1) || (r>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "969c96ace03541cead8cf85438c4f9de");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binarysearch2(arr, l, r, x);
}
