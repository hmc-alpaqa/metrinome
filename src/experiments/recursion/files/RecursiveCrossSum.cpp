int compute(int number) {
    if (number == 0) {
        return 0;
    }
    return (number % 10) + compute((int) number/10);
}