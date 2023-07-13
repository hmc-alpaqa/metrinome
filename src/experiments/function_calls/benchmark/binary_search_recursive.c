// Copied from src/experiments/recursion/files/binary-search.c

// Recursive version of binary search function
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