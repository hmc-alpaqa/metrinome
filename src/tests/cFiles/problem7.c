/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */

#include <stdlib.h>

int euler7(int n)
{
  char *sieve;
  int i;
  unsigned count = 0;
  const unsigned target = 10001;

  sieve = calloc(n, sizeof *sieve);
  for (i = 2; i < n; i++) {
    if (!sieve[i]) {
      int j;

      count++;
      if (count == target) {
        return i;
      }
      for (j = i*2; j < n; j += i) {
        sieve[j] = 1;
      }
    }
  }
  free(sieve);

  return 0;
}

