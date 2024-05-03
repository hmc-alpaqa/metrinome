/*
Write a Java program to find a character from a sentence and replace it with another character. If the character is not found in the string print "character not found".

Note: Replace only the first occurrence.

Sample input 1:

Enter the string:
java programming
Enter the character to be searched:
a
Enter the character to replace:
o

Sample output 1:

jova programming
*/
import java.util.Scanner;
class FirstOccurence
{
  public static void main (String[] args) {
    Scanner s=new Scanner(System.in);
    System.out.println("Enter the string:");
    String str=s.nextLine();
    System.out.println("Enter the character to be searched:");
    String sea=s.next();
    sea+=s.nextLine();
    System.out.println("Enter the character to replace:");
    String rep=s.next();
    rep+=s.nextLine();
    if(str.contains(sea))
    {
      str=str.replaceFirst(sea,rep);
       System.out.println(str);
    }
    else
      System.out.println("character not found");
  }
}
