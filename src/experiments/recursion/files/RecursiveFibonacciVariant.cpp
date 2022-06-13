int compute(int number) {
    if (number <= 1) {
        return 1;
    }
    return compute(number - 2) + compute(number - 4);
}