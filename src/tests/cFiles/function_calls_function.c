static int helper(int x) {
    while(x < 0) {
        ++x;
    }
    if (x < 0) {
        return -1;
    } else if (x >0){
        return 1;
    } else {
        return 0;
    }
} 

int main(int x){
    int value = helper(x);
    return value;
}

// int main() {
//     int x;
//     klee_make_symbolic(&x, sizeof(x), "x");
//     return outside_function(x);
// }