#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/heronian-triangles.c>
#define SIZE 10
int main() {

	list a;
	klee_make_symbolic(&a, sizeof(a), "e9aab3b06ee1452597789b491c168f49");

	int limit;
	klee_make_symbolic(&limit, sizeof(limit), "1667258f29004df4a1cc45ae3670c9bc");
	if ((limit<-1) || (limit>1024)) {
		 return 0;}

	int area;
	klee_make_symbolic(&area, sizeof(area), "3d5467b6e72044d4b590b863b8e53336");
	if ((area<-1) || (area>1024)) {
		 return 0;}
	printList(a, limit, area);
	return 0;
}
