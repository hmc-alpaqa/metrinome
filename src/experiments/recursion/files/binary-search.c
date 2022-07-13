#include <stdio.h>

int bsearch (int *a, int n, int x) {
    int i = 0, j = n - 1;
    while (i <= j) {
        int k = i + ((j - i) / 2);
        if (a[k] == x) {
            return k;
        }
        else if (a[k] < x) {
            i = k + 1;
        }
        else {
            j = k - 1;
        }
    }
    return -1;
}

int bsearch_r (int *a, int x, int i, int j) {
    if (j < i) {
        return -1;
    }
    int k = i + ((j - i) / 2);
    if (a[k] == x) {
        return k;
    }
    else if (a[k] < x) {
        return bsearch_r(a, x, k + 1, j);
    }
    else {
        return bsearch_r(a, x, i, k - 1);
    }
}
