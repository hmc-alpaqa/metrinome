/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */



int euler8(char str[])
{
  
  int len = sizeof str - 1;
  int i;
  unsigned max = 0;

  for (i = 0; i < len-4; i++) {
    unsigned p = 1;
    int j;

    for (j = 0; j < 5; j++) {
      p *= (unsigned)(str[i+j]-'0');
    }
    if (p > max) {
      max = p;
    }
  }
  
  return max;
}

