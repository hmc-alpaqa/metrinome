int array_function(int arr[]) { 
    int total = 0;
    for (int i = 0; i < 5; ++i)
        total += arr[i % 5];

    return total;
}   