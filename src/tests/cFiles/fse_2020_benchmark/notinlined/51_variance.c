double variance(double values[], int n)
{
    double sum = 0;
    for (int  i = 0; i < n; i++ )
        sum += values[i];

    double mean = sum / n;

    double var_sum = 0;

    for (int i = 0; i < n; i++ )
        var_sum += (values[i] - mean) * (values[i] - mean);
    return var_sum / (n - 1);
}
