#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/interpolation_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "9ca281fd7ff64fc5988d85ba7e40a105");

	int n;
	klee_make_symbolic(&n, sizeof(n), "66ac9b9e6fcb4153985f5f3514f534f7");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int key;
	klee_make_symbolic(&key, sizeof(key), "7254b4e767194cd8bd0c1220745854e1");
	if ((key<-1) || (key>1024)) {
		 return 0;}
	return interpolationSearch(arr, n, key);
}
