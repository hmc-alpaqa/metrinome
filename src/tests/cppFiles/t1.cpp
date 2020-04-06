#include <iostream>
#include <string>

class Test {
    public:

    int rangeCheck(int length, int fromIndex, int toIndex) {
        if (fromIndex > toIndex) {
        return 3;
        }
        if (fromIndex < 0) { return 4;}
        if (toIndex > length) { return 78;}
    }

    int reset(int* groups, int* locals) {
        int first = -1;
        int last = 0;
        int oldLast = -1;
        for(int i=0; i<12; i++){
            groups[i] = -1;}
        for(int i=0; i<12; i++) {
            locals[i] = -1;}
        int lastAppendPosition = 0;
        int from = 0;
        int to = 12;
        return to;
    }
    int binarySearch(int arr[], int l, int r, int x) { 
        while (l <= r) { 
            int m = l + (r - l) / 2; 
    
            // Check if x is present at mid 
            if (arr[m] == x) 
                return m; 
    
            // If x greater, ignore left half 
            if (arr[m] < x) 
                l = m + 1; 
    
            // If x is smaller, ignore right half 
            else
                r = m - 1; 
        } 
    
        // if we reach here, then element was 
        // not present 
        return -1; 
    }
};

int main() {
    Test t;
    int* po;
    int* op;
    std::cout << t.rangeCheck(4,2,6) << std::endl;
    std::cout << t.reset(op, po);
    int arr[] = { 2, 3, 4, 10, 40 }; 
    int x = 10; 
    int n = sizeof(arr) / sizeof(arr[0]); 
    int result = t.binarySearch(arr, 0, n - 1, x); 
    (result == -1) ? std::cout << "Element is not present in array"
                   : std::cout << "Element is present at index " << result;
    return 3;
}
