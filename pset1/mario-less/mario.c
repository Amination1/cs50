#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Enter hight : ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        for (int x = 0; x <= n - i - 2; x++)
        {
            printf(" ");
        }

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
