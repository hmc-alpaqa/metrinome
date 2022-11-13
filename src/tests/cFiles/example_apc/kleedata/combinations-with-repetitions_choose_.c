#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/combinations-with-repetitions.c>
#define SIZE 10
int main() {

	int *got;
	klee_make_symbolic(&got, sizeof(got), "f8cc07bb9ce2451b84bb395bc49b5189");

	int n_chosen;
	klee_make_symbolic(&n_chosen, sizeof(n_chosen), "cfca5d719a374da091403611fc21113a");
	if ((n_chosen<-1) || (n_chosen>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "e7864080b0194e928acd481b922d9930");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int at;
	klee_make_symbolic(&at, sizeof(at), "c422df1ba016422ba215a931e6ead9d6");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int max_types;
	klee_make_symbolic(&max_types, sizeof(max_types), "bd667f78ee774d80a32d3697b6f9d089");
	if ((max_types<-1) || (max_types>1024)) {
		 return 0;}
	return choose(got, n_chosen, len, at, max_types);
}
