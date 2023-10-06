// takes any integer n and returns n!, returns -1 for negative n
// apc case 1
// from src/tests/cFiles/rosetta-code-c/Factorial/factorial-4.c

int factorialSafe(int n) {
    return n<0 ? -1 : n == 0 ? 1 : n * factorialSafe(n - 1);
}
