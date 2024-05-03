import java.util.HashMap;
import java.util.Map;

/**
 * Counts the occurrence of characters in a string.
 * Punctuation marks and white spaces are also counted as characters.
 * 
 * This is done by iterating through all the characters of the string and count the letter in a map.
 * Finally the result is printed to system.out
 * 
 * Examples:
 * Input: test
 * Output:
 * 	s: 1
 *	t: 2
 *	e: 1
 *
 * Input: aaaaa
 * Output:
 * 	a: 5
 * 
 * Input: Hello world
 * Output:
 * 	 : 1
 *	!: 1
 *	r: 1
 *	d: 1
 *	e: 1
 *	w: 1
 *	H: 1
 *	l: 3
 *	o: 2
 */
public class CharacterCount {
	public static void main(String args[]) {
		String input = "Hello world!";
		
		Map<Character, Integer> characters = new HashMap<>();
		for (int i = 0; i < input.length(); ++i) {
			char c = input.charAt(i);
			if (characters.containsKey(c)) {
				characters.put(c, characters.get(c) + 1);
			} else {
				characters.put(c, 1);
			}
		}

		for (Map.Entry<Character, Integer> entry : characters.entrySet()) {
			System.out.println(entry.getKey() + ": " + entry.getValue());
		}
	}
}
