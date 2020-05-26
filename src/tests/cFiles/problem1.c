/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */



int euler1(int s3, int s5, int s15)
{
  int i;

  for (i = 0; i < 1000; i++) {
    if (i % 3 == 0) {
      s3 += i;
    }
    if (i % 5 == 0) {
      s5 += i;
    }
    if (i % 15 == 0) {
      s15 += i;
    }
  }
  

  return s3 + s5 - s15;
}
  
