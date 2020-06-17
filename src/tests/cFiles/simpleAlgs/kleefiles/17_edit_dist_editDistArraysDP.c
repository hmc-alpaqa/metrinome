#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/17_edit_dist.c>
#define SIZE 100
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "0bdae52fd4e34bf6ad2b707ac20f35ff");

	int b[SIZE];
	klee_make_symbolic(&b, sizeof(b), "ff83324cf51945e59e7400bb45d1a5b9");

	int m;
	klee_make_symbolic(&m, sizeof(m), "df1bd4f91fa9430aac87b6753cc95432");

	int n;
	klee_make_symbolic(&n, sizeof(n), "03ebf01e5de44421956ffbd05f71ac80");
	return editDistArraysDP(a, b, m, n);
}
