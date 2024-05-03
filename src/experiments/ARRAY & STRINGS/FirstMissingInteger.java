import java.util.Arrays;

/**
 * Given an unsorted integer array, find the first missing positive integer.
 * Example:
 * Given [1,2,0] return 3,
 * [3,4,-1,1] return 2,
 * [-8, -7, -6] returns 1
 * Your algorithm should run in O(n) time and use constant space.
 */
 
 
 public class FirstMissingInteger
{
  public static void main (String[] args) {
 // your code goes here
        int arr[] = {3,4,-1,1};
        int result =  firstMissingPositive(arr);
        System.out.println(result);
  }
  static int firstMissingPositive(int[] A)
    {
        Arrays.sort(A);
        int m=1;
        for(int i=0;i<A.length;i++)
        {
            if(A[i]>0)
            {
                if(m==A[i])
                    m++;
                else
                    return m;
            }
        }
        return m;
    }
}
 
 
/*
public class FirstMissingInteger {

    // Driver method
    public static void main (String[] args)
    {
        // your code goes here
        int arr[] = {3,4,-1,1};
        int result =  firstMissingPositive(arr);
        System.out.println(result);

    }

    static int firstMissingPositive(int[] A)
    {
        Arrays.sort(A);
        int m=1;
        for(int i=0;i<A.length;i++)
        {
            if(A[i]>0)
            {
                if(m==A[i])
                    m++;
                else
                    return m;
            }
        }
        return m;
    }

}
*/
