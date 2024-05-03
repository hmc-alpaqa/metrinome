import java.util.Scanner;
/**
 * This program reads an array of strings and prints "true" if the array
 * is in alphabetical order or "false" otherwise. The program uses the method
 * compareTo of the String class to compare two strings, s1 and s2, in
 * the following way:
 *
 * s1.compareTo(s2) will return -1 if s1 alphabetically precedes s2,
 * in the opposite case it will return 1, and finally, if the strings
 * are identical it will return 0.
 *
 * s1 alphabetically precedes s2 if the char s1[0] precedes the char s2[0],
 * if the chars are equal, the method compares the next chars, s1[1] and
 * s2[1], and so on. If a point is reached where one string has no more
 * chars left to compare then the shorter string is deemed to come first
 * in alphabetical order, e.g., "aa" precedes "aaa".
 */

public class AlphabeticalOrder {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String[] array = scanner.nextLine().split(" ");
        boolean alphabetical = true;

        for (int i = 0; i < array.length - 1; i++) {
            if (array[i].compareTo(array[i + 1]) > 0) {
                alphabetical = false;
                break;
            }
        }

        System.out.println(alphabetical);
        /*
        Sample input: a b c
        Output: true

        Sample input: aa a aaa
        Output: false
         */
    }
}
