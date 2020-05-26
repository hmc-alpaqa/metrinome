int array_function(int arr[], int length) { 
    int total = 0;
    for (int i = 0; i < length; ++i)
        total += arr[i];

    return total;
}   