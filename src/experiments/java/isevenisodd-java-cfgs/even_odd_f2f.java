public class FunctionCalls {
    public static void main(String[] args) {
        System.out.println(is_even_python(4)); // Output: true
        System.out.println(is_odd_python(4));  // Output: false
    }

    public static boolean is_even_python(int n) {
        if (n == 0) {
            return true;
        } else {
            return is_odd_python(n - 1);
        }
    }

    public static boolean is_odd_python(int n) {
        if (n == 0) {
            return false;
        } else {
            return is_even_python(n - 1);
        }
    }
}