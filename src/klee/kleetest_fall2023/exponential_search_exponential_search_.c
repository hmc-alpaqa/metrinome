#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/exponential_search.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	const int64_t arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "a349e907a97349e99c4729827fa08102");

	const uint16_t length;
	klee_make_symbolic(&length, sizeof(length), "c5ce51a9472f4cc997b63d568c92f9d0");
	if ((length<-1) || (length>1024)) {
		 return 0;}

	const int64_t n;
	klee_make_symbolic(&n, sizeof(n), "1bde591ae28d48df82207d466365aa11");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return exponential_search(arr, length, n);
}
