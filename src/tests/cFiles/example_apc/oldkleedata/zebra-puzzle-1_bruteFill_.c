#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/zebra-puzzle-1.c>
#define SIZE 10
int main() {

	int ha[5][5];
	klee_make_symbolic(&ha, sizeof(ha), "572ff2436dbb4a588e06d5020a314647");

	int hno;
	klee_make_symbolic(&hno, sizeof(hno), "30afd7f773504d22bccb009b02fe4d2c");
	if ((hno<-1) || (hno>1024)) {
		 return 0;}

	int attr;
	klee_make_symbolic(&attr, sizeof(attr), "e90360ba3d5f4503b1cf850319f059d0");
	if ((attr<-1) || (attr>1024)) {
		 return 0;}
	return bruteFill(ha, hno, attr);
}
