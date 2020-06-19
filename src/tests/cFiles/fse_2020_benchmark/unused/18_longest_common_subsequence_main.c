#include "18_longest_common_subsequence.c"

// The longest common subsequence in C

int main() {
  int S1[MAXSIZE] = {1,3,1,4,2}; //"ACADB"}; 
  int S2[MAXSIZE] = {3,2,4,1,2}; //"CBDA";
  int m = 5;
  int n = 5;

  // for(int i = 0; i < m; i++){
  // 	printf("%d ", S1[i]);
  // }
  // printf("\n");

  // for(int i = 0; i < n; i++){
  // 	printf("%d ", S2[i]);
  // }
  // printf("\n");

  int lcs_length = lcs(S1, m, S2, n);
  printf("LCS length = %d\n", lcs_length);
}




