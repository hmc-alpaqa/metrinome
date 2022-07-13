#include <stdio.h>
#include <ctype.h>

void rev_print(char *s, int n)
{
        for (; *s && isspace(*s); s++);
        if (*s) {
                char *e;
                for (e = s; *e && !isspace(*e); e++);
                rev_print(e, 0);
                printf("%.*s%s", (int)(e - s), s, " " + n);
        }
        if (n) putchar('\n');
}
