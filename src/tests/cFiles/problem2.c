/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */


int euler2(int a1, int a2,int a3)
{
  unsigned int sum = 0;

  while (a3 < 4000000) {
    a3 = a1 + a2;
    sum += a3 * !(a3%2);
    a1 = a2;
    a2 = a3;
  }

  return sum;
}

