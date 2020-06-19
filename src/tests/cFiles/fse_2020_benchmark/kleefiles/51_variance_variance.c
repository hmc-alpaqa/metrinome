#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/51_variance.c>
#define SIZE 100
int main() {

	double values[SIZE];
	klee_make_symbolic(&values, sizeof(values), "7789eaa1f8fe4690b3cce6eefc2a03e7");

	int n;
	klee_make_symbolic(&n, sizeof(n), "8f27969a45134d92aded276655cc4fb6");
	return variance(values, n);
}
