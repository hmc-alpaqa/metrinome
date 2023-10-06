#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	list a;
	klee_make_symbolic(&a, sizeof(a), "cc3c7a2da1624f4eab1384f174a9f0b1");

	int limit;
	klee_make_symbolic(&limit, sizeof(limit), "7bb8d2393c2a4b7890e0a4d0f4c4597d");
	if ((limit<-1) || (limit>1024)) {
		 return 0;}

	int area;
	klee_make_symbolic(&area, sizeof(area), "1ac0863897c94a348a14f071537bf877");
	if ((area<-1) || (area>1024)) {
		 return 0;}
	printList(a, limit, area);
	return 0;
}
