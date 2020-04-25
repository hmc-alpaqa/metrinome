
// klee fails
int recursive_func(int x) {
    if (x <= 0) 
        return 7;
    
    return recursive_func(x - 1);
}