#include <stdio.h>

#define uint unsigned int

void leafSearch(int level, uint child, int half, int len, int a[]);
void bottomUpSearch(int a[], int parents, uint child, int level, int tmp);
void rotateNodes(int a[], int level, uint child);

void heap_sort(int a[], uint len) {
  /* heap sort */
  uint half;
  uint parents;

  if (len <= 1) return;
  half = len >> 1;
  for (parents = half; parents >= 1; --parents) {
    int tmp;
    int level = 0;
    uint child;

    child = parents;
    /* bottom-up downheap */

    /* leaf-search for largest child path */
    leafSearch(level, child, half, len, a);

    /* bottom-up-search for rotation point */
    tmp = a[parents - 1];
    bottomUpSearch(a, parents, child, level, tmp);

    /* rotate nodes from parents to rotation point */
    rotateNodes(a, level, child);
    
    a[child - 1] = tmp;
  }

  --len;
  do {
    int tmp;
    int level = 0;
    uint child;

    /* move max element to back of array */
    tmp = a[len];
    a[len] = a[0];
    a[0] = tmp;

    child = parents = 1;
    half = len >> 1;

    /* bottom-up downheap */

    /* leaf-search for largest child path */
    leafSearch(level, child, half, len, a);

    /* bottom-up-search for rotation point */
    bottomUpSearch(a, parents, child, level, tmp);

    /* rotate nodes from parents to rotation point */
    rotateNodes(a, level, child);

    a[child - 1] = tmp;
  } while (--len >= 1);
}

/* leaf-search for largest child path */
void leafSearch(int level, uint child, int half, int len, int a[]){
  while (child <= half) {
    ++level;
    child += child;
    int comparison = (a[child] > a[child - 1]) ? 1 : (a[child] < a[child - 1]) ? -1 : 0;
    if ((child < len) && (comparison > 0))
      ++child;
  }
}

/* bottom-up-search for rotation point */
void bottomUpSearch(int a[], int parents, uint child, int level, int tmp){
  for (;;) {
    if (parents == child) break;
    int comparison = (tmp > a[child - 1]) ? 1 : (tmp < a[child - 1]) ? -1 : 0;
    if (comparison <= 0) break;
    child >>= 1;
    --level;
  }
}

void rotateNodes(int a[], int level, uint child){
  for (; level > 0; --level) {
    a[(child >> level) - 1] = a[(child >> (level - 1)) - 1];
  }
}

void display(int a[], const int size) {
  int i;
  for (i = 0; i < size; i++) printf("%d ", a[i]);

  printf("\n");
}

int main() {

  const int n = 10;
  int a[n] = {8, 5, 2, 3, 1, 6, 9, 4, 0, 7};

  printf("Array before sorting:\n");
  display(a, n);

  heap_sort(a, n);

  printf("Array after sorting:\n");
  display(a, n);

  return 0;
}
