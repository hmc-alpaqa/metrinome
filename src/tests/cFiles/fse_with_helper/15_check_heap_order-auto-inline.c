#include <iostream>
using namespace std;

// Iterative function to check if given array represents Min-Heap or not
__attribute__((always_inline)) inline bool checkMinHeap(int A[], int n) {
	// check for all internal nodes that their left child and
	// right child (if present) holds min-heap property or not
	for (int i = 0; i <= (n - 2) / 2; i++) {
		if (A[i] > A[2 * i + 1] || ((2 * i + 2 != n) && A[i] > A[2 * i + 2])) {
			return false;
		}
	}
	return true;
}

int main()
{
	int A[] = { 2, 3, 5, 8, 10 };
	int n = sizeof(A) / sizeof(int);

	if (checkMinHeap(A, n))
		cout << "Given array is a min heap";
	else
		cout << "Given array is not a min heap";

	return 0;
}