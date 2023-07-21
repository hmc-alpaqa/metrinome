// takes any integer n and returns n!, if n < 0, returns n itself
// apc case 1
// from src/tests/cFiles/rosetta-code-c/Factorial/factorial-5.c

int fac_aux(int n, int acc) {
    return n < 1 ? acc : fac_aux(n - 1, acc * n);
}

int fac_auxSafe(int n, int acc) {
    return n<0 ? -1 : n < 1 ? acc : fac_aux(n - 1, acc * n);
}