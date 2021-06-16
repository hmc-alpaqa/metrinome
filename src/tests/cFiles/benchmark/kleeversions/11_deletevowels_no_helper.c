#include <stdio.h>

int mainn(chat str[], int size)
{
    // char str[80];
    int i, j;

    // printf("Enter a string: ");
    // gets(str);
    int result;

    int x;
    int n = size;
    // char str[size];
    // srand(0);
    // for (x = 0; x < size; x++) {
    //     str[x] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random () % 26];
    // }

    for (i = 0, j = 0; str[i] != '\0'; i++)
    {
        switch (str[i])
        {
        case 'A':
        case 'a':
        case 'E':
        case 'e':
        case 'I':
        case 'i':
        case 'O':
        case 'o':
        case 'U':
        case 'u':
            result = 1;
        default:
            result = 0;
        }
        if (result == 0)
        {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';

    // printf("\nString without Vowels: %s", str);

    return 0;
}
