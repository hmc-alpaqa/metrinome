#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/11_array_max.c>
#define SIZE 100
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "ebc51c8d5a874d42a6f0b402c2c42b33");

	int num;
	klee_make_symbolic(&num, sizeof(num), "69e84d172279467a92cb3a0d2f0cadc1");
	return largest_element(arr, num);
}
