// function that finds the longest common substring of two strings
// apc case 1
// from src/experiments/recursion/files/example_apc_functions.c

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
char* longest_common_substring(char *a, char *b, int a_len, int b_len)
{
    int dp[a_len + 1][b_len + 1];
    // initialize the dp table
    for (int i = 0; i < a_len + 1; i++)
    {
        for (int j = 0; j < b_len + 1; j++)
        {
            dp[i][j] = 0;
        }
    }
    // fill the dp table
    int max = 0;
    int max_i = 0;
    int max_j = 0;
    for (int i = 1; i < a_len + 1; i++)
    {
        for (int j = 1; j < b_len + 1; j++)
        {
            if (a[i - 1] == b[j - 1])
            {
                // if the characters are the same, add 1 to the previous value to store the length of the longest common substring
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > max)
                {
                    max = dp[i][j];
                    max_i = i;
                    max_j = j;
                }
            }
            else
            {
                // if the characters are not equal, set the value to 0
                dp[i][j] = 0;
            }
        }
    }
    // create a string to store the longest common substring
    char *lcs = (char *)malloc((max + 1) * sizeof(char));
    // initialize the string
    for (int i = 0; i < max + 1; i++)
    {
        // set all characters to null
        lcs[i] = '\0';
    }
    // fill the string
    int i = max_i;
    int j = max_j;
    int k = max;
    while (i > 0 && j > 0)
    {
        if (a[i - 1] == b[j - 1])
        {
            lcs[k - 1] = a[i - 1];
            i--;
            j--;
            k--;
        }
        else
        {
            break;
        }
    }
    return lcs;
}