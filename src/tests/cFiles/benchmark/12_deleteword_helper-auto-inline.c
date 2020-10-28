#include <stdio.h>

__attribute__((always_inline)) inline int search(char[], char[]);
__attribute__((always_inline)) inline void delete_word(char[], char[], int);

int main()
{
    char str[80], word[50];
    int index;

    printf("Enter string:\n");
    gets(str);

    printf("Enter word to delete:\n");
    gets(word);

    index = search(str, word);

    if (index !=  - 1)
    {
        delete_word(str, word, index);
        printf("String without word:\n%s", str);
    }
    else
    {
        printf("The word not present in the string.");
    }

    return 0;
}

/* Function returns the index of str where word is found */
__attribute__((always_inline)) inline int search(char str[], char word[])
{
    int l, i, j;

    /* finding length of word */
    for (l = 0; word[l] != '\0'; l++);

    for (i = 0, j = 0; str[i] != '\0' && word[j] != '\0'; i++)
    {
        if (str[i] == word[j])
        {
            j++;
        }
        else
        {
            j = 0;
        }
    }

    if (j == l)
    {
        /* substring found */
        return (i - j);
    }
    else
    {
        return  - 1;
    }
}

__attribute__((always_inline)) inline void delete_word(char str[], char word[], int index)
{
    int i, l;
    
    /* finding length of word */
    for (l = 0; word[l] != '\0'; l++);

    for (i = index; str[i] != '\0'; i++)
    {
        str[i] = str[i + l + 1];
    }
}
