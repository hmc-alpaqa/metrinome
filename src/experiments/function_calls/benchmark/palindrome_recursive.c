// checks if an integer is a palindrome
// apc case 1
// from recursion/files/palindrome-detection-3.c

int palindrome_r(const char *s, int b, int e)
{
   if ( (e - 1) <= b ) return 1;
   if ( s[b] != s[e-1] ) return 0;
   return palindrome_r(s, b+1, e-1);
}
