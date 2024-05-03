import java.util.Scanner;
// Other imports go here
// Do NOT change the class name
class selectionSort
{
    static void selectionSort(int arr[],int n)
    {
        int min=arr[0];
        int temp=0;
        for(int i=0;i<n;i++)
        {
            min=i;
            for(int j=i+1;j<n;j++)
            {
                if(arr[min]>arr[j])
                {
                    min=j;
                }

            }
            temp=arr[min];
            arr[min]=arr[i];
            arr[i]=temp;
        }
    }
   
    public static void main(String[] args)
    {
        // Write your code here
        Scanner s=new Scanner(System.in);
        System.out.print("enter no of elements");
        int n=s.nextInt();
        int arr[]=new int[n];
        for(int i=0;i<n;i++)
        {
            arr[i]=s.nextInt();
        }
        selectionSort(arr,n);
        for(int i=0;i<n;i++)
        {
            System.out.print(arr[i]+" ");
        }
    }
    }
