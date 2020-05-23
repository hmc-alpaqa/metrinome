int first_func(int x) { 
    return x + 7;
}

// Klee fails
double second_func (int y) { 
    int total = 0;
    for (int i = 0; i < y; ++i) { 
        total += first_func(i);
    } 
    
    return total;
}