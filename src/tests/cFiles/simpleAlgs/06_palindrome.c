#include <stdio.h>

int palindrome(int num) {
  int reverse_num = 0, remainder, temp;
  temp = num;
  while (temp != 0) {
    remainder = temp % 10;
    reverse_num = reverse_num * 10 + remainder;
    temp /= 10;
  }
  return reverse_num == num;
}
