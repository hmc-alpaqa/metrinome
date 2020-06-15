int helper(int x) {
    if (x < 0) {
        return -1;
    } else {
        return 1;
    }
} 

int outside_function(int x){
    return helper(x);
}

// int main() {
//     int x;
//     klee_make_symbolic(&x, sizeof(x), "x");
//     return outside_function(x);
// }