#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/shell_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int array[SIZE][SIZE];
	klee_make_symbolic(&array, sizeof(array), "b156faf188a24bde846941a14241dff1");

	int len;
	klee_make_symbolic(&len, sizeof(len), "78e4768360654588b01ed8754c47d74f");
	if ((len<-1) || (len>1024)) {
		 return 0;}
	shellSort(array, len);
	return 0;
}
