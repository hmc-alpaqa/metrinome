#include <stdio.h>


void palindrome(int num){
  int reverse_num=0, remainder,temp;
  temp=num;
  while(temp!=0)
  {
     remainder=temp%10;
     reverse_num=reverse_num*10+remainder;
     temp/=10;
  }

  /* If the original input number (num) is equal to
   * to its reverse (reverse_num) then its palindrome
   * else it is not.
   */
  if(reverse_num==num)
     printf("%d is a palindrome number",num);
  else
     printf("%d is not a palindrome number",num);
}
int main()
{
   int num;
   printf("Enter an integer: ");
   scanf("%d", &num);
   palindrome(num);
}
