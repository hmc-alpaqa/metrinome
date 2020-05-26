/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */


int euler3(unsigned long long n)
{

  unsigned long long i;

  for (i = 2ULL; i < n; i++) {
    while (n % i == 0) {
      n /= i;
    }
  }


  return n;
}

