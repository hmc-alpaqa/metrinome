#include <stdio.h>

int data[] = {  85, 88, 75, 66, 25, 29, 83, 39, 97,
                68, 41, 10, 49, 16, 65, 32, 92, 28, 98 };

int pick(int at, int remain, int accu, int treat)
{
        if (!remain) return (accu > treat) ? 1 : 0;

        return  pick(at - 1, remain - 1, accu + data[at - 1], treat) +
                ( at > remain ? pick(at - 1, remain, accu, treat) : 0 );
}
