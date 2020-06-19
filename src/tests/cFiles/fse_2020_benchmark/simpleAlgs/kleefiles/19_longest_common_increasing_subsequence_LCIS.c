#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/19_longest_common_increasing_subsequence.c>
#define SIZE 100
int main() {

	int arr1[SIZE];
	klee_make_symbolic(&arr1, sizeof(arr1), "0f7679482c0a435ca62e6ea5e9b276fe");

	int n;
	klee_make_symbolic(&n, sizeof(n), "ad96ec4776874139b99dba4628a1aebd");

	int arr2[SIZE];
	klee_make_symbolic(&arr2, sizeof(arr2), "3c052e07f3f84f639d8eff5a01aaea26");

	int m;
	klee_make_symbolic(&m, sizeof(m), "d6d623e9c90547a1899a251c9384c9e9");
	return LCIS(arr1, n, arr2, m);
}
