#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/gnome_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int numbers[SIZE];
	klee_make_symbolic(&numbers, sizeof(numbers), "5b08f60a072343918d61adbbfb106648");

	int size;
	klee_make_symbolic(&size, sizeof(size), "05ce26cbb6344c268a8852ff10204edc");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	sort(numbers, size);
	return 0;
}
