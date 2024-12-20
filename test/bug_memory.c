#include <stdio.h>

int main(void)
{
    int me[10000];
    for (int i = 0; i < 10000; i++)
    {
        if (me[i] != 0)
        {
            printf("%c", me[i]);
        }
    }
}
