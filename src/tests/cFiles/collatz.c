int countCollatz(int n)
{
    int c = 0;
    while (n != 1)
    {
        ++c;
        if (n & 1) {
            n = 3 * n + 1;
        }
        else {
            n = n/2;
        }
    }

    return c;
}
