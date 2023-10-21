#include <stdio.h>

int fiveRecursiveHelper(int n);
int fiveRecursiveCalls(int n);

int nestedIf(int a, int b, int c) {
    if (a > 0) {
        if (b > 0) {
            return a;
        } else {
            return b;
        }
    } else {
        if (c > 0) {
            return c;
        } else {
            return a + b + c;
        }
    }
}

int nestedLoops(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            sum += 1;
        }
    }
    return sum;
}

int recursive(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return n + recursive(n - 1);
    }
}

int consecutiveLoops(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += 1;
    }
    for (int i = 0; i < n; i++) {
        sum += 1;
    }
    return sum;
}

int mixedNestedLoopsIfs(int n, int m) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        if (m > 0) {
            for (int j = 0; j < m; j++) {
                sum += 1;
            }
        } else {
            sum += 1;
        }
    }
    return sum;
}

int mixedRecursiveIfs(int n, int m) {
    if (n <= 0) {
        return m;
    } else {
        if (m > 0) {
            return n + mixedRecursiveIfs(n - 1, m - 1);
        } else {
            return n + mixedRecursiveIfs(n - 1, m);
        }
    }
}

int compositeFunction(int a, int b) {
    int result = nestedIf(a, b, recursive(a));
    return consecutiveLoops(result);
}

int nestedFunctionCalls(int n, int m) {
    if (mixedRecursiveIfs(n, m) > 0) {
        return nestedLoops(m);
    } else {
        for (int i = 0; i < n; i++) {
            m += recursive(i);
        }
        return m;
    }
}

int sequentialFunctionCalls(int n, int m) {
    int result1 = mixedNestedLoopsIfs(n, m);
    int result2 = nestedIf(result1, n, m);
    return recursive(result2);
}

int recursiveCombination(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return nestedIf(n, recursiveCombination(n - 1), n - 1);
    }
}

int combinedStrategies(int n, int m) {
    int result = compositeFunction(n, m);
    if (nestedFunctionCalls(result, m) > 0) {
        return sequentialFunctionCalls(n, result);
    } else {
        return recursiveCombination(m);
    }
}

int chainedFunctions(int n, int m) {
    int res1 = nestedLoops(n);
    int res2 = consecutiveLoops(res1);
    int res3 = mixedNestedLoopsIfs(res2, m);
    return recursive(res3);
}

int nestedRecursion(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return recursive(recursive(n - 1));
    }
}

int loopsWithMultipleFunctionCalls(int n, int m) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += mixedNestedLoopsIfs(i, m);
        sum += recursive(i);
    }
    return sum;
}

int ifElseLadder(int n, int m) {
    if (n > m) {
        return recursive(n);
    } else if (n < m) {
        return nestedLoops(m);
    } else {
        return consecutiveLoops(n + m);
    }
}

int combinedLoopsConditionsRecursion(int n, int m) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        if (mixedRecursiveIfs(i, m) > 0) {
            sum += recursive(i);
        } else {
            sum += mixedNestedLoopsIfs(i, m);
        }
    }
    return sum;
}

int nestedFunctionsWithRecursionLoops(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return nestedLoops(n) + nestedFunctionsWithRecursionLoops(n - 1);
    }
}

int combineFunctionResults(int n, int m) {
    int res1 = nestedIf(n, m, n + m);
    int res2 = consecutiveLoops(res1);
    int res3 = mixedNestedLoopsIfs(res2, m);
    return recursive(res1 + res2 + res3);
}

int diverseRecursiveCalls(int n) {
    if (n <= 0) {
        return 1;
    } else if (n % 2 == 0) {
        return nestedLoops(n) + diverseRecursiveCalls(n - 1);
    } else {
        return recursive(n) + diverseRecursiveCalls(n - 1);
    }
}

int triangleRecursion(int n) {
    int res = 1;
    if (n <= 0) {
        return 2; 
    }
    for (int i = 1; i <= n; i++) {
        res += triangleRecursion(n - i);
    }
    return res;
}

int tonsOfLoops(int n, int m) {
    int loopCount = sequentialFunctionCalls(n, m);
    int res = 0;
    for (int i = 0; i < loopCount; i++) {
        for (int j = 0; j < n; j++) {
            res += j;
        }
    }
    return res;
}

int tonsOfLoopsAndRecursion(int n, int m) {
    int loopCount = sequentialFunctionCalls(n, m);
    int res = 0;
    for (int i = 0; i < loopCount; i++) {
        for (int j = 0; j < n; j++) {
            res += diverseRecursiveCalls(j);
        }
    }
    return res;
}

int hundredConsecutiveLoops(int n) {
    int res = 0;
    for (int i = n; i < 1; i++) res += i;
    for (int i = n; i < 2; i++) res += i;
    for (int i = n; i < 3; i++) res += i;
    for (int i = n; i < 4; i++) res += i;
    for (int i = n; i < 5; i++) res += i;
    for (int i = n; i < 6; i++) res += i;
    for (int i = n; i < 7; i++) res += i;
    for (int i = n; i < 8; i++) res += i;
    for (int i = n; i < 9; i++) res += i;
    for (int i = n; i < 10; i++) res += i;
    for (int i = n; i < 11; i++) res += i;
    for (int i = n; i < 12; i++) res += i;
    for (int i = n; i < 13; i++) res += i;
    for (int i = n; i < 14; i++) res += i;
    for (int i = n; i < 15; i++) res += i;
    for (int i = n; i < 16; i++) res += i;
    for (int i = n; i < 17; i++) res += i;
    for (int i = n; i < 18; i++) res += i;
    for (int i = n; i < 19; i++) res += i;
    for (int i = n; i < 20; i++) res += i;
    for (int i = n; i < 21; i++) res += i;
    for (int i = n; i < 22; i++) res += i;
    for (int i = n; i < 23; i++) res += i;
    for (int i = n; i < 24; i++) res += i;
    for (int i = n; i < 25; i++) res += i;
    for (int i = n; i < 26; i++) res += i;
    for (int i = n; i < 27; i++) res += i;
    for (int i = n; i < 28; i++) res += i;
    for (int i = n; i < 29; i++) res += i;
    for (int i = n; i < 30; i++) res += i;
    for (int i = n; i < 31; i++) res += i;
    for (int i = n; i < 32; i++) res += i;
    for (int i = n; i < 33; i++) res += i;
    for (int i = n; i < 34; i++) res += i;
    for (int i = n; i < 35; i++) res += i;
    for (int i = n; i < 36; i++) res += i;
    for (int i = n; i < 37; i++) res += i;
    for (int i = n; i < 38; i++) res += i;
    for (int i = n; i < 39; i++) res += i;
    for (int i = n; i < 40; i++) res += i;
    for (int i = n; i < 41; i++) res += i;
    for (int i = n; i < 42; i++) res += i;
    for (int i = n; i < 43; i++) res += i;
    for (int i = n; i < 44; i++) res += i;
    for (int i = n; i < 45; i++) res += i;
    for (int i = n; i < 46; i++) res += i;
    for (int i = n; i < 47; i++) res += i;
    for (int i = n; i < 48; i++) res += i;
    for (int i = n; i < 49; i++) res += i;
    for (int i = n; i < 50; i++) res += i;
    for (int i = n; i < 51; i++) res += i;
    for (int i = n; i < 52; i++) res += i;
    for (int i = n; i < 53; i++) res += i;
    for (int i = n; i < 54; i++) res += i;
    for (int i = n; i < 55; i++) res += i;
    for (int i = n; i < 56; i++) res += i;
    for (int i = n; i < 57; i++) res += i;
    for (int i = n; i < 58; i++) res += i;
    for (int i = n; i < 59; i++) res += i;
    for (int i = n; i < 60; i++) res += i;
    for (int i = n; i < 61; i++) res += i;
    for (int i = n; i < 62; i++) res += i;
    for (int i = n; i < 63; i++) res += i;
    for (int i = n; i < 64; i++) res += i;
    for (int i = n; i < 65; i++) res += i;
    for (int i = n; i < 66; i++) res += i;
    for (int i = n; i < 67; i++) res += i;
    for (int i = n; i < 68; i++) res += i;
    for (int i = n; i < 69; i++) res += i;
    for (int i = n; i < 70; i++) res += i;
    for (int i = n; i < 71; i++) res += i;
    for (int i = n; i < 72; i++) res += i;
    for (int i = n; i < 73; i++) res += i;
    for (int i = n; i < 74; i++) res += i;
    for (int i = n; i < 75; i++) res += i;
    for (int i = n; i < 76; i++) res += i;
    for (int i = n; i < 77; i++) res += i;
    for (int i = n; i < 78; i++) res += i;
    for (int i = n; i < 79; i++) res += i;
    for (int i = n; i < 80; i++) res += i;
    for (int i = n; i < 81; i++) res += i;
    for (int i = n; i < 82; i++) res += i;
    for (int i = n; i < 83; i++) res += i;
    for (int i = n; i < 84; i++) res += i;
    for (int i = n; i < 85; i++) res += i;
    for (int i = n; i < 86; i++) res += i;
    for (int i = n; i < 87; i++) res += i;
    for (int i = n; i < 88; i++) res += i;
    for (int i = n; i < 89; i++) res += i;
    for (int i = n; i < 90; i++) res += i;
    for (int i = n; i < 91; i++) res += i;
    for (int i = n; i < 92; i++) res += i;
    for (int i = n; i < 93; i++) res += i;
    for (int i = n; i < 94; i++) res += i;
    for (int i = n; i < 95; i++) res += i;
    for (int i = n; i < 96; i++) res += i;
    for (int i = n; i < 97; i++) res += i;
    for (int i = n; i < 98; i++) res += i;
    for (int i = n; i < 99; i++) res += i;
    return res;
}

int fiveRecursiveHelper(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return fiveRecursiveCalls(n - 1);
    }
}

int fiveRecursiveCalls(int n) {
    int res = 0;
    if (n <= 0) {
        return 1;
    }
    for (int i = 0; i < 1; i++) res += fiveRecursiveHelper(n);
    for (int i = 0; i < 2; i++) res += fiveRecursiveHelper(n);
    for (int i = 0; i < 3; i++) res += fiveRecursiveHelper(n);
    // // printf("res: %d\n", res);
    // for (int i = n; i < 4; i++) res += fiveRecursiveHelper(i);
    // // printf("res: %d\n", res);
    // for (int i = n; i < 5; i++) res += fiveRecursiveHelper(i);
    printf("res: %d\n", res);

    return res;
}

int tripleNestedRecursion(int n, int m) {
    if (n <= 0) {
        return nestedFunctionCalls(m, n);
    }
    return recursiveCombination(nestedFunctionCalls(n, m));
}

int consecutiveLoopsWithNestedCalls(int n, int m) {
    int sum = 0;
    for (int i = 0; i < nestedLoops(n); i++) {
        sum += mixedNestedLoopsIfs(i, m);
    }
    for (int i = 0; i < consecutiveLoops(n); i++) {
        sum += mixedRecursiveIfs(i, m);
    }
    return sum;
}

int deepIfElseLadder(int n, int m) {
    if (nestedIf(n, m, n + m) > 0) {
        return nestedFunctionCalls(n, m);
    } else if (consecutiveLoops(n + m) > n) {
        return compositeFunction(n, m);
    } else {
        return sequentialFunctionCalls(n, m);
    }
}

int loopWithComposite(int n, int m) {
    int sum = 0;
    for (int i = 0; i < compositeFunction(n, m); i++) {
        sum += mixedNestedLoopsIfs(i, nestedIf(i, n, m));
    }
    return sum;
}

int recursiveWithNested(int n, int m) {
    if (n <= 0) {
        return nestedIf(m, n, m + n);
    }
    return mixedNestedLoopsIfs(n, m) + recursiveWithNested(n - 1, m);
}

int switchWithComposite(int n, int m) {
    switch (compositeFunction(n, m)) {
        case 0:
            return nestedLoops(m);
        case 1:
            return recursive(n);
        default:
            return nestedIf(n, m, n + m);
    }
}

int main() {
    printf("nestedIf: %d\n", nestedIf(1, -2, 3));
    printf("nestedLoops: %d\n", nestedLoops(3));
    printf("recursive: %d\n", recursive(4));
    printf("consecutiveLoops: %d\n", consecutiveLoops(5));
    printf("mixedNestedLoopsIfs: %d\n", mixedNestedLoopsIfs(2, 3));
    printf("mixedRecursiveIfs: %d\n", mixedRecursiveIfs(3, 2));
    printf("compositeFunction: %d\n", compositeFunction(3, 4));
    printf("nestedFunctionCalls: %d\n", nestedFunctionCalls(3, 4));
    printf("sequentialFunctionCalls: %d\n", sequentialFunctionCalls(3, 4));
    printf("recursiveCombination: %d\n", recursiveCombination(3));
    printf("combinedStrategies: %d\n", combinedStrategies(3, 4));
    printf("chainedFunctions: %d\n", chainedFunctions(3, 4));
    printf("nestedRecursion: %d\n", nestedRecursion(3));
    printf("loopsWithMultipleFunctionCalls: %d\n",
           loopsWithMultipleFunctionCalls(3, 4));
    printf("ifElseLadder: %d\n", ifElseLadder(3, 4));
    printf("combinedLoopsConditionsRecursion: %d\n",
           combinedLoopsConditionsRecursion(3, 4));
    printf("nestedFunctionsWithRecursionLoops: %d\n",
           nestedFunctionsWithRecursionLoops(3));
    printf("combineFunctionResults: %d\n", combineFunctionResults(3, 4));
    printf("diverseRecursiveCalls: %d\n", diverseRecursiveCalls(3));
    printf("triangleRecursion: %d\n", triangleRecursion(10));
    printf("tonsOfLoops: %d\n", tonsOfLoops(3, 4));
    printf("tonsOfLoopsAndRecursion: %d\n", tonsOfLoopsAndRecursion(3, 4));
    printf("hundredConsecutiveLoops: %d\n", hundredConsecutiveLoops(3));
    printf("hundredRecursiveCalls: %d\n", fiveRecursiveCalls(0));
    printf("tripleNestedRecursion: %d\n", tripleNestedRecursion(3, 4));
    printf("consecutiveLoopsWithNestedCalls: %d\n",
           consecutiveLoopsWithNestedCalls(3, 4));
    printf("deepIfElseLadder: %d\n", deepIfElseLadder(3, 4));
    printf("loopWithComposite: %d\n", loopWithComposite(3, 4));
    printf("recursiveWithNested: %d\n", recursiveWithNested(3, 4));
    printf("switchWithComposite: %d\n", switchWithComposite(3, 4));
    return 0;
}
