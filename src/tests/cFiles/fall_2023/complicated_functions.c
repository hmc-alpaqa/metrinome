#include <stdio.h>

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

// int main() {
//     printf("nestedIf: %d\n", nestedIf(1, -2, 3));
//     printf("nestedLoops: %d\n", nestedLoops(3));
//     printf("recursive: %d\n", recursive(4));
//     printf("consecutiveLoops: %d\n", consecutiveLoops(5));
//     printf("mixedNestedLoopsIfs: %d\n", mixedNestedLoopsIfs(2, 3));
//     printf("mixedRecursiveIfs: %d\n", mixedRecursiveIfs(3, 2));
//     printf("compositeFunction: %d\n", compositeFunction(3, 4));
//     printf("nestedFunctionCalls: %d\n", nestedFunctionCalls(3, 4));
//     printf("sequentialFunctionCalls: %d\n", sequentialFunctionCalls(3, 4));
//     printf("recursiveCombination: %d\n", recursiveCombination(3));
//     printf("combinedStrategies: %d\n", combinedStrategies(3, 4));
//     printf("chainedFunctions: %d\n", chainedFunctions(3, 4));
//     printf("nestedRecursion: %d\n", nestedRecursion(3));
//     printf("loopsWithMultipleFunctionCalls: %d\n",
//            loopsWithMultipleFunctionCalls(3, 4));
//     printf("ifElseLadder: %d\n", ifElseLadder(3, 4));
//     printf("combinedLoopsConditionsRecursion: %d\n",
//            combinedLoopsConditionsRecursion(3, 4));
//     printf("nestedFunctionsWithRecursionLoops: %d\n",
//            nestedFunctionsWithRecursionLoops(3));
//     printf("combineFunctionResults: %d\n", combineFunctionResults(3, 4));
//     printf("diverseRecursiveCalls: %d\n", diverseRecursiveCalls(3));
//     printf("triangleRecursion: %d\n", triangleRecursion(10));
//     printf("tonsOfLoops: %d\n", tonsOfLoops(3, 4));
//     return 0;
// }
