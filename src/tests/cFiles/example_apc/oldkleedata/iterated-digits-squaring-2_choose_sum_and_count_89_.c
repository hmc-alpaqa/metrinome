#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	int *got;
	klee_make_symbolic(&got, sizeof(got), "654ccb367f31496aa5312b5926bb3de2");

	int n_chosen;
	klee_make_symbolic(&n_chosen, sizeof(n_chosen), "9329be9ae4624ca8baceb4e3babad291");
	if ((n_chosen<-1) || (n_chosen>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "cf234224efb24b05bcda3908ed3f98aa");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int at;
	klee_make_symbolic(&at, sizeof(at), "993edb300c0741a1839b8e14f6db6a18");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int max_types;
	klee_make_symbolic(&max_types, sizeof(max_types), "3b91e109a58d464d9c78f0690cd9425e");
	if ((max_types<-1) || (max_types>1024)) {
		 return 0;}

	int *count89;
	klee_make_symbolic(&count89, sizeof(count89), "379646a3a3174a62aa8cd87439d77d40");
	return choose_sum_and_count_89(got, n_chosen, len, at, max_types, count89);
}
