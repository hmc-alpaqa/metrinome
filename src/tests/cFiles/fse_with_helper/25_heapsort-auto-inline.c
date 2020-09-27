#include <stdio.h>
#include <stdlib.h>

#define uint unsigned int
#define SIZE 10

typedef int (*compare_func)(int, int);

__attribute__((always_inline)) inline int compare(int a, int b);
__attribute__((always_inline)) inline void heap_sort(int a[], compare_func func_pointer, uint len);
__attribute__((always_inline)) inline void display(int a[],const int size);

int main()
{
    int a[SIZE] = {8,5,2,3,1,6,9,4,0,7};

    printf("Array before sorting:\n");
    display(a,SIZE);

    heap_sort(a, compare, SIZE);

    printf("Array after sorting:\n");
    display(a,SIZE);

    return 0;
}

__attribute__((always_inline)) inline int compare(int a, int b)
{
    if (a > b)
        return 1;
    else if (a < b)
        return -1;
    else
        return 0;
}

__attribute__((always_inline)) inline void heap_sort(int a[], compare_func func_pointer, uint len)
{
    /* heap sort */
    uint half;
    uint parents;

    if (len <= 1)
        return;
    half = len >> 1;
    for (parents = half; parents >= 1; --parents)
    {
        int tmp;
        int level = 0;
        uint child;

        child = parents;
        /* bottom-up downheap */

        /* leaf-search for largest child path */
        while (child <= half)
        {
            ++level;
            child += child;
            if ((child < len) &&  ((*func_pointer)(a[child], a[child - 1]) > 0))
                ++child;
        }
        /* bottom-up-search for rotation point */
        tmp = a[parents - 1];
        for (;;)
        {
            if (parents == child)
                break;
            if ((*func_pointer)(tmp, a[child - 1]) <= 0)
                break;
            child >>= 1;
            --level;
        }
        /* rotate nodes from parents to rotation point */
        for (; level > 0; --level)
        {
            a[(child >> level) - 1] =
                a[(child >> (level - 1)) - 1];
        }
        a[child - 1] = tmp;
    }

    --len;
    do
    {
        int tmp;
        int level = 0;
        uint child;

        /* move max element to back of array */
        tmp = a[len];
        a[len] = a[0];
        a[0] = tmp;

        child = parents = 1;
        half = len >> 1;

        /* bottom-up downheap */

        /* leaf-search for largest child path */
        while (child <= half)
        {
            ++level;
            child += child;
            if ((child < len) && ((*func_pointer)(a[child], a[child - 1]) > 0))
                ++child;
        }
        /* bottom-up-search for rotation point */
        for (;;)
        {
            if (parents == child)
                break;
            if ((*func_pointer)(tmp, a[child - 1]) <= 0)
                break;
            child >>= 1;
            --level;
        }
        /* rotate nodes from parents to rotation point */
        for (; level > 0; --level)
        {
            a[(child >> level) - 1] =
                a[(child >> (level - 1)) - 1];
        }
        a[child - 1] = tmp;
    }
    while (--len >= 1);
}

__attribute__((always_inline)) inline void display(int a[],const int size)
{
    int i;
    for(i = 0; i < size; i++)
        printf("%d ",a[i]);

    printf("\n");
}
