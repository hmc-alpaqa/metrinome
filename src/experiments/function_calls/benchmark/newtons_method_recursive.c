// function that finds the approximation of a n-root of a number using newton's method
//copied from recursive/files/fibonacci_test.c

double newtons_method_rec(double number, int root, double guess)
{
    double value = 1;
    for (int i = 0; i < root - 1; i++) {
        value *= guess;
    }
    double new_guess = guess - (value * guess - number) / (root * value);
    if (new_guess == guess) {
        return guess;
    } else {
        return newtons_method_rec(number, root, new_guess);
    }
}