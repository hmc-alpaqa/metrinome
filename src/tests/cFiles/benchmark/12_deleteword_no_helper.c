#include <stdio.h>

int search(char[], char[]);
void delete_word(char[], char[], int);

int main()
{
    char str[80], word[50];
    int index;

    printf("Enter string:\n");
    gets(str);

    printf("Enter word to delete:\n");
    gets(word);

    
    // SEARCH 
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
        index =  (i - j);
    }
    else
    {
        index =  - 1;
    }

    if (index !=  - 1)
    {
        // DELETE WORD

        int i, l;
        /* finding length of word */
        for (l = 0; word[l] != '\0'; l++);

        for (i = index; str[i] != '\0'; i++)
        {
            str[i] = str[i + l + 1];
        }

        printf("String without word:\n%s", str);
    }
    else
    {
        printf("The word not present in the string.");
    }

    return 0;
}
