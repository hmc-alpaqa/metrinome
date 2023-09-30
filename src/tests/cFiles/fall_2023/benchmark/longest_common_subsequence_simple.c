#include <limits.h>
#include <stdio.h>
#include <stdlib.h>


char* longest_common_subsequence(char *a, char *b, int a_len, int b_len)
{
    // create a dp table to store the longest common subsequence
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
    for (int i = 1; i < a_len + 1; i++)
    {
        for (int j = 1; j < b_len + 1; j++)
        {
            if (a[i - 1] == b[j - 1])
            {
                // if the characters are the same, add 1 to the previous value to store the length of the longest common subsequence
                dp[i][j] = dp[i - 1][j - 1] + 1;
            }
            else
            {
                // if the characters are not equal, take the max of the previous row and column
                dp[i][j] = dp[i - 1][j] > dp[i][j - 1] ? dp[i - 1][j] : dp[i][j - 1];
            }
        }
    }
    // create a string to store the longest common subsequence
    char* lcs = (char *)malloc((dp[a_len][b_len] + 1) * sizeof(char));
    // initialize the string
    for (int i = 0; i < dp[a_len][b_len] + 1; i++)
    {
        // set all characters to null
        lcs[i] = '\0';
    }
    // fill the string
    int i = a_len;
    int j = b_len;
    int k = dp[a_len][b_len];
    while (i > 0 && j > 0)
    {
        if (a[i - 1] == b[j - 1])
        {
            lcs[k - 1] = a[i - 1];
            i--;
            j--;
            k--;
        }
        else if (dp[i - 1][j] > dp[i][j - 1])
        {
            i--;
        }
        else
        {
            j--;
        }
    }
    return lcs;
}