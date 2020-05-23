// klee fails

int nested_loops_func(int x, int y) {
    int sum = 0;
    for(int i = 0; i < x; i++) {
        if (i%178 == 123){
            sum = sum + i;
        }
        if (i == 213) {
            return 23;
        }
        for (int j = 0; j < y; j++) {
            sum++;
        }
    }
    if (sum == 345) {
        return -1;
    }
    return sum;
}