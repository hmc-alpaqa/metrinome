/*
 * Copyright (c) 2009, eagletmt
 * Released under the MIT License <http://opensource.org/licenses/mit-license.php>
 */


static unsigned long gcd(unsigned long a, unsigned long b);
static unsigned long lcm(unsigned long a, unsigned long b);

int euler5(unsigned long ans)
{

  unsigned long i;

  for (i = 1; i <= 20; i++) {
    ans = lcm(ans, i);
  }
  return ans;
}

unsigned long gcd(unsigned long a, unsigned long b)
{
  unsigned long r;

  if (a > b) {
    unsigned long t = a;
    a = b;
    b = t;
  }

  while (r = a%b) {
    a = b;
    b = r;
  }
  return b;
}

unsigned long lcm(unsigned long a, unsigned long b)
{
  unsigned long long p = (unsigned long long)a * b;
  return p/gcd(a, b);
}
