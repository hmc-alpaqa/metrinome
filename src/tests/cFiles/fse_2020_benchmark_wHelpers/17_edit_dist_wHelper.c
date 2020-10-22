#include <stdio.h>

#define MAXSIZE 100

void helperFunction(int a[], int b[], int m, int n, int dp[][MAXSIZE + 1], int i);

int editDistArraysDP(int a[], int b[], int m, int n) {
  // Create a table to store results of subproblems
  int dp[MAXSIZE + 1][MAXSIZE + 1];
  // int u = 0, v = 0, w = 0;

  // Fill d[][] in bottom up manner
  for (int i = 0; i <= m; i++) {
    // Originally nested for loop
    helperFunction(a, b, m, n, dp, i);
  }
  return dp[m][n];
}

// should edit dp in place (hence void)
void helperFunction(int a[], int b[], int m, int n, int dp[][MAXSIZE + 1], int i){
  for (int j = 0; j <= n; j++) {
      // If first string is empty, only option is to
      // insert all characters of second string
      if (i == 0) dp[i][j] = j;  // Min. operations = j

      // If second string is empty, only option is to
      // remove all characters of second string
      else if (j == 0)
        dp[i][j] = i;  // Min. operations = i

      // If last characters are same, ignore last char
      // and recur for remaining string
      else if (a[i - 1] == b[j - 1])
        dp[i][j] = dp[i - 1][j - 1];

      // If the last character is different, consider all
      // possibilities and find the minimum
      else {
        int minimum;
        int x = dp[i][j - 1];      // Insert
        int y = dp[i - 1][j];      // Remove
        int z = dp[i - 1][j - 1];  // Replace
        // dp[i][j] = 1 + min(x,y,z);

        if (x < y) {
          minimum = x;
        } else {
          minimum = y;
        }
        if (z < minimum) {
          minimum = z;
        }
        dp[i][j] = 1 + minimum;
      }
  }
}