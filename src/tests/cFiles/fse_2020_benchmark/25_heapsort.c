#include <stdio.h>

#define uint unsigned int

__attribute__((always_inline)) inline void heap_sort(int a[], uint len) {
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
    while (child <= half) {
      ++level;
      child += child;
      int comparison = (a[child] > a[child - 1]) ? 1 : (a[child] < a[child - 1]) ? -1 : 0;
      if ((child < len) && (comparison > 0))
        ++child;
    }
    /* bottom-up-search for rotation point */
    tmp = a[parents - 1];
    for (;;) {
      if (parents == child) break;
      int comparison = (tmp > a[child - 1]) ? 1 : (tmp < a[child - 1]) ? -1 : 0;
      if (comparison <= 0) break;
      child >>= 1;
      --level;
    }
    /* rotate nodes from parents to rotation point */
    for (; level > 0; --level) {
      a[(child >> level) - 1] = a[(child >> (level - 1)) - 1];
    }
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
    while (child <= half) {
      ++level;
      child += child;
      int comparison = (a[child] > a[child - 1]) ? 1 : (a[child] < a[child - 1]) ? -1 : 0;
      if ((child < len) && (comparison > 0))
        ++child;
    }
    /* bottom-up-search for rotation point */
    for (;;) {
      if (parents == child) break;
      int comparison = (tmp > a[child - 1]) ? 1 : (tmp < a[child - 1]) ? -1 : 0;
      if (comparison <= 0) break;
      child >>= 1;
      --level;
    }
    /* rotate nodes from parents to rotation point */
    for (; level > 0; --level) {
      a[(child >> level) - 1] = a[(child >> (level - 1)) - 1];
    }
    a[child - 1] = tmp;
  } while (--len >= 1);
}


