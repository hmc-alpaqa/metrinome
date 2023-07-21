#include <stdio.h>

int isVowel(char ch);

int main()
{
    char str[80];
    int i, j;

    printf("Enter a string: ");
    gets(str);

    for (i = 0, j = 0; str[i] != '\0'; i++)
    {
        if (!isVowel(str[i]))
        {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';

    printf("\nString without Vowels: %s", str);

    return 0;
}

int isVowel(char ch)
{
    switch (ch)
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
            return 1;
        default:
            return 0;
    }
}
