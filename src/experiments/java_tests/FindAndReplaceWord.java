/*

[Search and replace should be case sensitive.  Input can contain words separated by space and full stop.]

Sample Input 1:

Enter the string:

Have a good day

Enter the word to be searched:

good

Enter the word to be replaced:

nice

Sample Output 1:

Have a nice day

Sample Input 2:

Enter the string:

Have a good day

Enter the word to be searched:

nice

Enter the word to be replaced:

nice

Sample Output 2:

The word nice not found



Sample Input 3:

Enter the string:
Google PlayStore is a digital distribution service operated and developed by Google.

Enter the word to be searched:

Google

Enter the word to be replaced:

Yahoo

Sample Output 3:

Yahoo PlayStore is a digital distribution service operated and developed by Yahoo.
*/
import java.util.Arrays;
import java.util.Scanner;
public class FindAndReplaceWord
{
  public static void main (String[] args) {
    Scanner s=new Scanner(System.in);
    System.out.println("Enter the String:");
    String str=s.nextLine();
    System.out.println("Enter the word to be searched:");
    String sea=s.next();
    sea+=s.nextLine();
    System.out.println("Enter the word to be replaced:");
    String rep=s.next();
    rep+=s.nextLine();
    if(str.contains(sea))
      str=str.replaceAll(sea,rep);
    else
    {
      System.out.println("The word "+sea+" not found");
      System.exit(0);
    }
    System.out.println(str);
  }
}
