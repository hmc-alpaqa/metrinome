#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/cocktail_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "dda29ba50f4f4c418d16ad6da1f7bd5f");

	int size;
	klee_make_symbolic(&size, sizeof(size), "53e53ce12b84435a91481de1edcc6ac4");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	cocktailSort(arr, size);
	return 0;
}
