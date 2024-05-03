import java.util.Arrays;
import java.util.Scanner;
class ArraySorting
{
  public static void main (String[] args) {
    Scanner s=new Scanner(System.in);
    System.out.println("Enter array length:");
    int length=s.nextInt();
    int [] numArray = new int[length];
    for( int i = 0; i<length; i++){
    System.out.println("Enter number for index " + i + ":");
    int num=s.nextInt();
    numArray[i] = num;
    }
    System.out.println("Original numeric array : "+Arrays.toString(numArray));
    Arrays.sort(numArray);  
    System.out.println("Sorted numeric array : "+Arrays.toString(numArray)); 
  }
}
