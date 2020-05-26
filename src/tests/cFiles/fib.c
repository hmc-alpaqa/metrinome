int bounded_fib(int n) {
    int n1 = 0; 
    int n2 = 1;
    int count = 0;

    while(count < n && count < 100){
       int nth;
       nth = n1 + n2;
    
       n1 = n2;
       n2 = nth;

       count++;
    }
    return n1;
}
