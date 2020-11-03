double findSum(double values[], int n);
double findVarSum(double values[], int n, double mean);

double variance(double values[], int n)
{
    double sum = findSum(values, n);
    double mean = sum / n;
    double var_sum = findVarSum(values, n, mean);
    
    return var_sum / (n - 1);
}

double findSum(double values[], int n){
    double sum = 0; 
    for (int  i = 0; i < n; i++ )
        sum += values[i];
    return sum;
}

double findVarSum(double values[], int n, double mean){
    double var_sum = 0;
    for (int i = 0; i < n; i++ )
        var_sum += (values[i] - mean) * (values[i] - mean);
    return var_sum;
}