/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */



int euler9(int x)
{
  int a, b, p;

  for (a = 1; a <= x; a++) {
    for (b = a; b <= 666; b++) {
      int c = (1000 - a - b);
      if (a*a + b*b == c*c) {
        p = a * b * c;
      }
    }
  }
  return p;
}
