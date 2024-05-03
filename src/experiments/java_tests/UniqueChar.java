/*Print unique characters
Write a program to print all the unique characters in a given sentence. 

The sentence should have only alphabets .

If the sentence is not valid display the message "Invalid Sentence".

If unique characters are not found print "No unique characters".

If unique characters are found print those characters as shown in sample output.

Sample Input 1:
Enter the sentence:
java is an object oriented programming language

Sample Output 1:
Unique characters:
v
s
b
c
d
p
l
u

Sample Input 2:
Welcome to 12house

Sample Output 2:
Invalid Sentence*/

import java.util.*;
public class UniqueChar
{
    public static void main(String args[])
    {
        Scanner scn = new Scanner(System.in);
        System.out.println("Enter the sentence:");
        String input=scn.nextLine();
        Map<Character,Integer>hashMap = new LinkedHashMap<>();
        for(int i=0;i<input.length();i++)
        {
            if(Character.isAlphabetic(input.charAt(i))||input.charAt(i)==' ')
            {
                if(hashMap.containsKey(input.charAt(i)))
                {
                    hashMap.put(input.charAt(i),hashMap.get(input.charAt(i))+1);
                }
                else
                {
                    hashMap.put(input.charAt(i),1);
                }
            }
            else
            {
                System.out.println("Invalid Sentence");
                return;
            }
        }
        int flag=0;
        ArrayList<Character> arrls=new ArrayList<>();
        for(Map.Entry entry: hashMap.entrySet())
        {
            if((int)entry.getValue()==1)
            {
                arrls.add((char)entry.getKey());
                flag+=1;
            }
        }
        if(flag>0)
        {
            System.out.println("Unique characters:");
            for(int i=0;i<arrls.size();i++)
            {
                System.out.println(arrls.get(i));
            }
        }
        else if(flag==0)
        {
            System.out.println("No unique characters");
        }
    }
}
