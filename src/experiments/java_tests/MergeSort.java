/**
 * @author Adam Walker
 * 
 *  Java program to demonstrate Merge Sort
 */
public class MergeSort {

    /**
     * 
     * @param arr merges two sub arrays from arr[]
     * @param left the left half of arr[], from left -> middle
     * @param middle mid point of arr[]
     * @param right the right half of arr [], from middle + 1 -> right
     */
    public void merge(int[] arr, int left, int middle, int right){

        // find size of sub arrays
        int array1Size = middle - left + 1;
        int array2Size = right - middle; 

        // create sub arrays
        int[] array1 = new int[array1Size];
        int[] array2 = new int[array2Size];

        // fill data to sub arrays
        for (int i = 0; i < array1Size; ++i){
            array1[i] = arr[left + i];
        }
        for (int j = 0; j < array2Size; ++j){
            array2[j] = arr[middle + 1 + j];
        }

        // indicies for subarrays
        int i=0;
        int j=0;
        int k=left;

        // merge elements from subarrays to one array
        while (i < array1Size && j < array2Size){
            if (array1[i] <= array2[j]){
                arr[k] = array1[i];
                i++;
            }
            else{
                arr[k] = array2[j];
                j++;
            }
            k++;
        }

        while (i < array1Size){
            arr[k] = array1[i];
            i++;
            k++;
        }

        while (j < array2Size){
            arr[k] = array2[j];
            j++;
            k++;
        }
    }

    // sorts arr[] using merge()
    public void sort(int[] arr, int left, int right){
        if (left < right){
            int middle = (left + right) / 2;

            sort(arr, left, middle);
            sort(arr, middle + 1, right);

            merge(arr, left, middle, right);
        }
    }

    public static void main(String[] args){
        //sample array
        int[] array = {4, 1, 5, 9, 3, 2, 10, 6, 7, 0, 8};

        System.out.println("Sample array: ");
        for (int i = 0; i < array.length; i++){
            System.out.print( array[i] + " ");
        }
        System.out.println();

        // sort array
        MergeSort mergeObj = new MergeSort();
        mergeObj.sort(array, 0, array.length-1);

        System.out.println("Sorted array: ");
        for (int i = 0; i < array.length; i++){
            System.out.print( array[i] + " ");
        }
    }

}