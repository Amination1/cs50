#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int nn = 0;
    int n;
    do
    {
        n = get_int("Enter : ");
    }
    while (n < 0);

    while (n >= 25)
    {
        nn += 1;
        n -= 25;
    }
    while (n >= 10)
    {
        nn += 1;
        n -= 10;
    }
    while (n >= 5)
    {
        nn += 1;
        n -= 5;
    }
    while (n >= 1)
    {
        nn += 1;
        n -= 1;
    }
    printf("%d\n", nn);
}
