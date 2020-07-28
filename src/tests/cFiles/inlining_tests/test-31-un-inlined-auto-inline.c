#include <math.h>
#include <stdio.h>
#include <stdlib.h>

struct triangle {
  int a;
  int b;
  int c;
};

typedef struct triangle triangle;
__attribute__((always_inline)) inline int area(triangle t) {
  return ((t.a + t.b + t.c) * (t.a + t.b - t.c) * (t.a + t.c - t.b) *
          (t.b + t.c - t.a));
}
__attribute__((always_inline)) inline void sort_by_area(triangle* tr, int n) {
  for (int i = 0; i < n - 1; i++)
    for (int j = i + 1; j < n; j++)
      if (area(tr[i]) > area(tr[j])) {
        triangle t = tr[i];
        tr[i] = tr[j];
        tr[j] = t;
      }
}

int main() {
  int n;
  scanf("%d", &n);
  triangle* tr = malloc(n * sizeof(triangle));
  for (int i = 0; i < n; i++) {
    scanf("%d%d%d", &tr[i].a, &tr[i].b, &tr[i].c);
  }
  sort_by_area(tr, n);
  for (int i = 0; i < n; i++) {
    printf("%d %d %d\n", tr[i].a, tr[i].b, tr[i].c);
  }
  return 0;
}