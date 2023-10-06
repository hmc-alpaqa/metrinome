#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	int *got;
	klee_make_symbolic(&got, sizeof(got), "ffd530774a614de3bcadefdf8f8875b4");

	int n_chosen;
	klee_make_symbolic(&n_chosen, sizeof(n_chosen), "4524326caaf148069ad9ae08a2229a92");
	if ((n_chosen<-1) || (n_chosen>1024)) {
		 return 0;}

	int len;
	klee_make_symbolic(&len, sizeof(len), "7901b18937ae49eeaebb0811e91f2417");
	if ((len<-1) || (len>1024)) {
		 return 0;}

	int at;
	klee_make_symbolic(&at, sizeof(at), "4db57ba5b3dc4ad0a344fffe8a4ddb79");
	if ((at<-1) || (at>1024)) {
		 return 0;}

	int max_types;
	klee_make_symbolic(&max_types, sizeof(max_types), "92180908458144e691ea74fd4633d4e6");
	if ((max_types<-1) || (max_types>1024)) {
		 return 0;}

	int *count89;
	klee_make_symbolic(&count89, sizeof(count89), "53150a27f3c4444c99282fa630d06690");
	return choose_sum_and_count_89(got, n_chosen, len, at, max_types, count89);
}
