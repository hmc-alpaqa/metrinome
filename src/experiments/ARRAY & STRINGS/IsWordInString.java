 
/**
  * Checks if a given word is in the input string
  *
  * Sample input string one "Hello world!"
  * Sample input word "Hello"
  *
  * Sample output "Found word"
  *
  */

import java.util.Scanner;

public class IsWordInString {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        
        System.out.print("Type a string: ");
        String text = s.nextLine();
        System.out.println();
        System.out.print("Enter the word to find: ");
        String word = s.nextLine();
        System.out.println();
        
        
        if (text.toLowerCase().contains(word.toLowerCase())) {
            System.out.println("Found word \"" + word + "\" in text \"" + text + "\"!");
        } else {
            System.out.println("Word not found!");
        }
    }
}
