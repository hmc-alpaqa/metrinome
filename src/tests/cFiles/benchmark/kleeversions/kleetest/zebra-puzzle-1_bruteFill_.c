#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "ef0b6c1935b74bf5bf4a47a01c327a0a");

	int hno;
	klee_make_symbolic(&hno, sizeof(hno), "c29164f635c24818b4af15f1f8f384eb");
	if ((hno<-1) || (hno>1024)) {
		 return 0;}

	int attr;
	klee_make_symbolic(&attr, sizeof(attr), "9dfbd5b409f840a19d5bc9ac28dab1f4");
	if ((attr<-1) || (attr>1024)) {
		 return 0;}
	return bruteFill(ha, hno, attr);
}
