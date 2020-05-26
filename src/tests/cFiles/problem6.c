/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */

int euler6(unsigned s1, unsigned s2)
{
  unsigned i;

  for (i = 1; i <= 100; i++) {
    s1 += i*i;
    s2 += i;
  }
  
  return s2*s2 - s1;
}

