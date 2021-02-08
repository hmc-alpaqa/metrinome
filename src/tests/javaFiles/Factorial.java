public class Factorial {

	public static void test(int n)
	{	int result = 1;
		for(int i = 2; i <= n; i++)
			result *= i;
		System.out.println(result);
	}

}