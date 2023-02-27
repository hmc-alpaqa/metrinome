#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/combinations-with-repetitions.c>
#define SIZE 10
int main() {

	int *got;
	klee_make_symbolic(&got, sizeof(got), "332469eb6b6345abab395f5d80686a70");

	int n_chosen;
	klee_make_symbolic(&n_chosen, sizeof(n_chosen), "1a471707af9446419b7638bf3b20141c");
	if ((n_chosen<-1) || (n_chosen>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "e75f046998f24a06857f1807e7b7b680");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int at;
	klee_make_symbolic(&at, sizeof(at), "62f8dd2b10c04af58f5305d81475a90d");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int max_types;
	klee_make_symbolic(&max_types, sizeof(max_types), "402ee878ab414d45a95592bf194f4082");
	if ((max_types<-1) || (max_types>1024)) {
		 return 0;}
	return choose(got, n_chosen, len, at, max_types);
}
