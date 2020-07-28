// Valid Palindrome

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

char ch2lower(char ch) {
  if (ch >= 'A' && ch <= 'Z') ch += 0x20;

  return ch;
}

bool isPalindrome(char *s) {
  int len = strlen(s);
  int head, tail;
  head = tail = 0;
  tail = len - 1;

  while (head <= tail) {
    while (ch2lower(s[head]) < '0' ||
           (ch2lower(s[head]) > '9' && ch2lower(s[head]) < 'a') ||
           ch2lower(s[head]) > 'z') {
      head++;
      if (head > tail) break;
    }

    while (ch2lower(s[tail]) < '0' ||
           (ch2lower(s[tail]) > '9' && ch2lower(s[tail]) < 'a') ||
           ch2lower(s[tail]) > 'z') {
      tail--;
      if (head > tail) break;
    }

    if (head > tail) break;

    if (ch2lower(s[head]) != ch2lower(s[tail])) return false;

    head++;
    tail--;
  }

  return true;
}

int main() {
  char s1[] = "A man, a plan, a canal: Panama";

  printf("%d\n", isPalindrome(s1));

  return 0;
}